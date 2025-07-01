import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from telebot import TeleBot
from app.handlers import text
import os
from dotenv import load_dotenv
from app.handlers import file
from app.handlers import voice
from app.handlers import summarize
from app.handlers import tts

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# ✅ Dict global unruk simpan preferensi bahasa per user
user_lang = {}

# Registrasi handler dengan parameter user_lang
text.register(bot, user_lang)
file.register(bot)
#voice.register(bot)
summarize.register(bot)
tts.register(bot)

# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

