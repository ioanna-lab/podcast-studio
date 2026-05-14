# 🎙️ The Daily Brief — Podcast Studio

An automated podcast generator that turns any news article URL or live Hacker News top stories into a fully produced audio episode using OpenAI GPT-4o-mini and OpenAI TTS.

## What It Does

Paste a URL or pick Hacker News → get a podcast script + audio file in under 30 seconds.

**Pipelines:**
```
Article URL  →  Extract text  →  LLM script  →  OpenAI TTS  →  MP3
HN API       →  Top N stories →  LLM script  →  OpenAI TTS  →  MP3
```

## Project Structure

```
podcast-studio/
├── src/
│   ├── data_processor.py    # Fetches and extracts text from article URLs
│   ├── llm_processor.py     # Transforms content into podcast script via GPT-4o-mini
│   ├── tts_generator.py     # Converts script to audio via OpenAI TTS
│   ├── hn_processor.py      # Fetches top stories from Hacker News API (no key needed)
│   └── main.py              # Gradio interface — two tabs, full pipeline
├── requirements.txt
├── README.md
└── .env                     # API keys (not committed)
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/podcast-studio.git
cd podcast-studio
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Create your `.env` file
```
OPENAI_API_KEY=sk-proj-...
```

### 4. Run the app
```bash
cd src && python3 main.py
```

Open **http://127.0.0.1:7860** in your browser.

## How to Use

### Tab 1 — Article URL
1. Paste any news article URL
2. Click **Generate Podcast**
3. Read the script and play the audio

### Tab 2 — Hacker News
1. Use the slider to choose how many top stories to include (3-10)
2. Click **Generate HN Brief**
3. Get a live tech news podcast from today's top Hacker News stories

## Hacker News API

No API key required. Uses the free public Firebase API:

```python
import requests

# Get top story IDs
story_ids = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json"
).json()[:5]

# Get details for one story
story = requests.get(
    f"https://hacker-news.firebaseio.com/v0/item/{story_ids[0]}.json"
).json()

print(story["title"], story["score"], story["url"])
```

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.8+ |
| Frontend | Gradio |
| Article extraction | BeautifulSoup4 + Requests |
| News API | Hacker News Firebase API (free) |
| LLM | OpenAI GPT-4o-mini |
| Text-to-Speech | OpenAI TTS (voice: alloy) |

## Notes

- Works best with publicly accessible article URLs (BBC, Reuters, Guardian, etc.)
- Paywalled articles return a clear error message
- Content capped at 5,000 characters to stay within token limits
- Audio saved as `podcast_output.mp3` (URL tab) or `hn_output.mp3` (HN tab)
