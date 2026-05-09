import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_audio(script: dict, output_path: str = "output.mp3") -> dict:
    """
    Takes a podcast script dictionary and generates an audio file.
    Returns a dictionary with the audio file path and metadata.
    """
    try:
        if "error" in script:
            return {"error": script["error"]}

        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",   # options: alloy, echo, fable, onyx, nova, shimmer
            input=script["script"]
        )

        # Save the audio file
        output_file = Path(output_path)
        with open(output_file, "wb") as f:
            f.write(response.content)

        return {
            "title": script["title"],
            "audio_path": str(output_file),
            "script": script["script"]
        }

    except Exception as e:
        return {"error": f"Audio generation failed: {str(e)}"}


# Quick test
if __name__ == "__main__":
    sample_script = {
        "title": "Test Episode",
        "script": "Welcome to The Daily Brief. Scientists have discovered a new species of deep sea fish in the Pacific Ocean. The fish, named Deepsea Wonderfish, can survive at depths of 8000 meters. Researchers from MIT conducted the study over three years. That's your Daily Brief. Stay informed."
    }

    result = generate_audio(sample_script, output_path="test_output.mp3")

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"✅ Audio generated successfully!")
        print(f"File saved to: {result['audio_path']}")