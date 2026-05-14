import gradio as gr
import os
from dotenv import load_dotenv
from data_processor import fetch_article
from llm_processor import generate_podcast_script
from tts_generator import generate_audio
from hn_processor import fetch_hn_briefing

load_dotenv()

def generate_from_url(url: str):
    """Pipeline: URL → article → script → audio"""
    if not url.strip():
        return "Please enter a URL.", None

    print(f"Fetching article from: {url}")
    article = fetch_article(url)
    if "error" in article:
        return f"Error fetching article: {article['error']}", None

    print("Generating podcast script...")
    script = generate_podcast_script(article)
    if "error" in script:
        return f"Error generating script: {script['error']}", None

    print("Generating audio...")
    audio = generate_audio(script, output_path="podcast_output.mp3")
    if "error" in audio:
        return f"Error generating audio: {audio['error']}", None

    return script["script"], "podcast_output.mp3"


def generate_from_hn(limit: int):
    """Pipeline: Hacker News top stories → script → audio"""
    print(f"Fetching top {limit} stories from Hacker News...")
    article = fetch_hn_briefing(limit=int(limit))
    if "error" in article:
        return f"Error fetching HN stories: {article['error']}", None

    print("Generating podcast script...")
    script = generate_podcast_script(article)
    if "error" in script:
        return f"Error generating script: {script['error']}", None

    print("Generating audio...")
    audio = generate_audio(script, output_path="hn_output.mp3")
    if "error" in audio:
        return f"Error generating audio: {audio['error']}", None

    return script["script"], "hn_output.mp3"


# Build Gradio interface with two tabs
with gr.Blocks(title="The Daily Brief — Podcast Studio") as app:

    gr.Markdown("# 🎙️ The Daily Brief")
    gr.Markdown("Generate an instant podcast episode from a news article or Hacker News top stories.")

    with gr.Tabs():

        # Tab 1 — Article URL
        with gr.TabItem("📰 Article URL"):
            gr.Markdown("Paste any news article URL and get a podcast episode.")
            with gr.Row():
                url_input = gr.Textbox(
                    label="Article URL",
                    placeholder="https://www.bbc.com/news/...",
                    scale=4
                )
                url_btn = gr.Button("Generate Podcast 🎧", variant="primary", scale=1)

            url_script = gr.Textbox(label="Podcast Script", lines=10, interactive=False)
            url_audio = gr.Audio(label="Your Podcast Episode", type="filepath")

            url_btn.click(
                fn=generate_from_url,
                inputs=[url_input],
                outputs=[url_script, url_audio]
            )

        # Tab 2 — Hacker News
        with gr.TabItem("🔥 Hacker News"):
            gr.Markdown("Generate a tech briefing from today's Hacker News top stories.")
            with gr.Row():
                hn_limit = gr.Slider(
                    minimum=3,
                    maximum=10,
                    value=5,
                    step=1,
                    label="Number of stories",
                    scale=4
                )
                hn_btn = gr.Button("Generate HN Brief 🎧", variant="primary", scale=1)

            hn_script = gr.Textbox(label="Podcast Script", lines=10, interactive=False)
            hn_audio = gr.Audio(label="Your HN Brief Episode", type="filepath")

            hn_btn.click(
                fn=generate_from_hn,
                inputs=[hn_limit],
                outputs=[hn_script, hn_audio]
            )

    gr.Markdown("---")
    gr.Markdown("*Powered by OpenAI GPT-4o-mini and OpenAI TTS*")

if __name__ == "__main__":
    app.launch()