import os
from dotenv import load_dotenv

# Load variabel dari .env
load_dotenv()

# === Client 1: Groq (untuk Chat GPT) ===
from openai import OpenAI as GroqClient

groq_client = GroqClient(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# === Client 2: OpenAI (untuk Transkripsi Suara) ===
from openai import OpenAI as OpenAIClient

openai_client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY")  # Ini API dari OpenAI asli
)

# === Chat GPT pakai Groq ===
def ask_gpt(prompt: str, lang: str = "id") -> str:
    try:
        instruction = {
            "id": "Jawablah pertanyaan berikut dalam Bahasa Indonesia.",
            "en": "Answer the following question in English."
        }.get(lang, "Jawablah pertanyaan berikut dalam Bahasa Indonesia.")

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Terjadi error: {e}"

# === Transkripsi Voice pakai OpenAI ===
def transcribe_audio(audio_filepath):
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        return f"❌ Error saat transkripsi: {e}"

