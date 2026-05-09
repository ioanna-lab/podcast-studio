# 🎙️ The Daily Brief — Podcast Studio

An automated news podcast generator that turns any article URL into a fully produced audio episode using OpenAI GPT-4o-mini and OpenAI TTS.

## What It Does

Paste a news article URL → get a podcast script + audio file in under 30 seconds.

**Pipeline:**
```
Article URL → Extract text → LLM generates script → OpenAI TTS → Audio file
```

## Project Structure

```
podcast-studio/
├── src/
│   ├── data_processor.py    # Fetches and extracts text from article URLs
│   ├── llm_processor.py     # Transforms article into podcast script via GPT-4o-mini
│   ├── tts_generator.py     # Converts script to audio via OpenAI TTS
│   └── main.py              # Gradio interface — connects the full pipeline
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
Create a `.env` file in the root folder:
```
OPENAI_API_KEY=sk-proj-...
```

### 4. Run the app
```bash
cd src && python3 main.py
```

Then open your browser at **http://127.0.0.1:7860**

## How to Use

1. Paste any news article URL into the input field
2. Click **Generate Podcast**
3. Wait ~20-30 seconds
4. Read the generated script and play the audio episode

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.8+ |
| Frontend | Gradio |
| Article extraction | BeautifulSoup4 |
| LLM | OpenAI GPT-4o-mini |
| Text-to-Speech | OpenAI TTS (voice: alloy) |

## Example Output

Input URL: `https://www.bbc.com/news`

Generated script:
> Welcome to The Daily Brief. Today, we're diving into some significant global headlines. Tensions are rising as Iran accuses the U.S. of breaching a recent truce... That's your Daily Brief. Stay informed.

Audio: ~60-90 second MP3 episode

## Notes

- Works best with article URLs that have clear paragraph text (BBC, Reuters, Guardian, etc.)
- Content is limited to 5000 characters to stay within token limits
- Audio is saved as `podcast_output.mp3` in the `src/` folder
