import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_podcast_script(article: dict) -> dict:
    """
    Takes an article dictionary and transforms it into a podcast script.
    Returns a dictionary with the script and metadata.
    """
    try:
        if "error" in article:
            return {"error": article["error"]}

        prompt = f"""
You are a professional podcast host for a daily news brief called "The Daily Brief".

Transform the following article into a short, engaging podcast script (90-120 seconds when read aloud).

Guidelines:
- Start with a warm welcome: "Welcome to The Daily Brief."
- Summarize the key points in a conversational, friendly tone
- Use natural spoken language — no bullet points, no markdown
- Add smooth transitions between points
- End with a sign-off: "That's your Daily Brief. Stay informed."
- Keep it between 150-200 words

Article title: {article['title']}
Article content: {article['content']}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        script = response.choices[0].message.content.strip()

        return {
            "title": article["title"],
            "url": article.get("url", ""),
            "script": script
        }

    except Exception as e:
        return {"error": f"LLM processing failed: {str(e)}"}


# Quick test
if __name__ == "__main__":
    # Test with a sample article
    sample_article = {
        "title": "Test Article",
        "content": "Scientists have discovered a new species of deep sea fish in the Pacific Ocean. The fish, named Deepsea Wonderfish, can survive at depths of 8000 meters. Researchers from MIT conducted the study over three years using underwater drones. The discovery sheds new light on biodiversity in extreme environments.",
        "url": "https://example.com"
    }

    result = generate_podcast_script(sample_article)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Title: {result['title']}")
        print(f"\nScript:\n{result['script']}")