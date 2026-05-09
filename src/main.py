import gradio as gr
import os
from dotenv import load_dotenv
from data_processor import fetch_article
from llm_processor import generate_podcast_script
from tts_generator import generate_audio

load_dotenv()

def generate_podcast(url: str):
    """
    Full pipeline: URL → article → script → audio
    """
    if not url.strip():
        return "Please enter a URL.", None

    # Step 1: Fetch article
    print(f"Fetching article from: {url}")
    article = fetch_article(url)
    if "error" in article:
        return f"Error fetching article: {article['error']}", None

    # Step 2: Generate podcast script
    print("Generating podcast script...")
    script = generate_podcast_script(article)
    if "error" in script:
        return f"Error generating script: {script['error']}", None

    # Step 3: Generate audio
    print("Generating audio...")
    audio_path = "podcast_output.mp3"
    audio = generate_audio(script, output_path=audio_path)
    if "error" in audio:
        return f"Error generating audio: {audio['error']}", None

    # Return script text and audio file
    return script["script"], audio_path


# Build Gradio interface
with gr.Blocks(title="The Daily Brief — Podcast Studio") as app:

    gr.Markdown("# 🎙️ The Daily Brief")
    gr.Markdown("Paste a news article URL and get an instant podcast episode.")

    with gr.Row():
        url_input = gr.Textbox(
            label="Article URL",
            placeholder="https://www.bbc.com/news/...",
            scale=4
        )
        generate_btn = gr.Button("Generate Podcast 🎧", variant="primary", scale=1)

    with gr.Row():
        script_output = gr.Textbox(
            label="Podcast Script",
            lines=10,
            interactive=False
        )

    with gr.Row():
        audio_output = gr.Audio(
            label="Your Podcast Episode",
            type="filepath"
        )

    generate_btn.click(
        fn=generate_podcast,
        inputs=[url_input],
        outputs=[script_output, audio_output]
    )

    gr.Markdown("---")
    gr.Markdown("*Powered by OpenAI GPT-4o-mini and OpenAI TTS*")

if __name__ == "__main__":
    app.launch()