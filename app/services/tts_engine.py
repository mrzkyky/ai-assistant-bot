from gtts import gTTS
import os
import time

def text_to_speech(text: str, lang: str = "id") -> str:
    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"tts_{int(time.time())}.mp3"
        filepath = os.path.join("downloads", filename)
        tts.save(filepath)
        return filepath
    except Exception as e:
        print(f"❌ Error saat TTS: {e}")
        return None
