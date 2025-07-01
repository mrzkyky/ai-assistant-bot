import os
from telebot.types import Message
from app.services.file_reader import read_file_content
from app.services.openai_client import ask_gpt

def register(bot):
    @bot.message_handler(commands=["summarizefile"])
    def handle_summarize_file(message: Message):
        try:
            parts = message.text.strip().split()
            if len(parts) != 2:
                bot.reply_to(message, "⚠️ Gunakan format: /summarizefile <namafile>")
                return

            filename = parts[1]
            filepath = os.path.join("downloads", filename)

            if not os.path.exists(filepath):
                bot.reply_to(message, "❌ File tidak ditemukan.")
                return

            text = read_file_content(filepath)
            if not text:
                bot.reply_to(message, "❌ File kosong atau gagal dibaca.")
                return

            prompt = f"Buatkan ringkasan isi file berikut secara singkat:\n\n{text[:4000]}"
            summary = ask_gpt(prompt)
            bot.reply_to(message, f"📄 Ringkasan:\n\n{summary}")

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

