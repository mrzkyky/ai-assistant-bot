import os
from telebot.types import Message
from app.services.openai_client import transcribe_audio
from telebot import TeleBot

DOWNLOAD_DIR = "downloads"

def register(bot: TeleBot):
    @bot.message_handler(content_types=['voice', 'audio'])
    def handle_voice(message: Message):
        file_id = None
        if message.content_type == 'voice':
            file_id = message.voice.file_id
        elif message.content_type == 'audio':
            file_id = message.audio.file_id
        else:
            return bot.reply_to(message, "❌ Tipe file audio tidak didukung.")

        file_info = bot.get_file(file_id)
        file_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.ogg")

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        file_data = bot.download_file(file_info.file_path)

        with open(file_path, 'wb') as f:
            f.write(file_data)

        bot.reply_to(message, "🎙️ Sedang mengubah suara ke teks...")

        # Panggil fungsi transcribe_audio di openai_client.py
        text = transcribe_audio(file_path)

        if text:
            bot.send_message(message.chat.id, f"📝 Transkripsi:\n\n{text}")
        else:
            bot.send_message(message.chat.id, "❌ Gagal transkripsi audio.")

















