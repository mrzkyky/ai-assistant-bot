import os
from telebot.types import Message
from app.services.file_reader import read_file_content
from app.services.openai_client import ask_gpt


DOWNLOAD_DIR = "downloads"

# File yang diizinkan dibaca sebagai teks
ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.py', '.js', '.json', '.yaml', '.yml', '.html', '.md', '.css', '.csv', '.xml', '.ini', '.sh', '.conf']

def register(bot):
    # Handler untuk file yang dikirim user 
    @bot.message_handler(content_types=['document'])
    def handle_document(message: Message):
        doc = message.document
        file_ext = os.path.splitext(doc.file_name)[1].lower()

        if file_ext not in ALLOWED_EXTENSIONS:
            return bot.reply_to(message, "❗ Jenis file tidak didukung. Hanya file teks seperti .txt, .pdf, .py, dll.")
        
        # Ambil info dan data file dari Telegram
        file_info = bot.get_file(doc.file_id)
        file_data = bot.download_file(file_info.file_path)

        # Buat folder downloads jika belum ada
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        file_path = os.path.join(DOWNLOAD_DIR, doc.file_name)

        # Simpan file ke server 
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Baca dan balas isi file
        content = read_file_content(file_path)
        if content:
            preview = content[:1000] + ("..." if len(content) > 1000 else "")
            bot.reply_to(
                message,
                f"📄 Isi file *{doc.file_name}*:\n\n```{preview}```",
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(message, "❌ Gagal membaca file.")

    # Handler untuk perintah /explainfile
    @bot.message_handler(commands=['explainfile'])
    def handle_explainfile(message: Message):
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return bot.reply_to(message, "❗ Gunakan format: /explainfile <nama_file>")

        filename = parts[1].strip()
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        if not os.path.exists(filepath):
            return bot.reply_to(message, f"❌ File *{filename}* tidak ditemukan.", parse_mode="Markdown")

        # Baca isi file dan batasi panjang karakter (bisa naik jadi 10000)
        content = read_file_content(filepath)
        if not content:
            return bot.reply_to(message, "❌ Gagal membaca isi file.")

        prompt = (
            f"Berikut adalah isi file `{filename}`:\n\n"
            f"{content[:10000]}\n\n"
            "Tolong:\n"
            "- Jelaskan fungsinya\n"
            "- Sederhanakan jika bisa\n"
            "- Deteksi potensi bug atau kekurangan"
        )

        bot.reply_to(message, "🔍 Memproses penjelasan file dengan AI...")
        result = ask_gpt(prompt)
        bot.send_message(
            message.chat.id,
            f"📘 Penjelasan untuk *{filename}*:\n\n{result}",
            parse_mode="Markdown"
        )
