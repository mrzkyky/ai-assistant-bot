import os
from telebot.types import Message
from app.services.tts_engine import text_to_speech

def register(bot):
    @bot.message_handler(commands=["say"])
    def handle_say(message: Message):
        text = message.text.replace("/say", "").strip()

        if not text:
            bot.reply_to(message, "⚠️ Format: /say <teks yang ingin diubah menjadi suara>")
            return

        audio_path = text_to_speech(text)
        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as audio_file:
                bot.send_audio(message.chat.id, audio_file, caption="🔊 Ini hasil TTS-mu")
        else:
            bot.reply_to(message, "❌ Gagal mengubah teks jadi suara.")

