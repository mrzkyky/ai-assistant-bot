from app.services.openai_client import ask_gpt

def register(bot, user_lang):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, "👋 Hai! Aku asisten AI-mu.\nKetik /ask untuk bertanya.")

    @bot.message_handler(commands=['lang'])
    def handle_lang(message):
        args = message.text.split()
        if len(args) < 2 or args[1] not in ["id", "en"]:
            return bot.reply_to(message, "❗ Gunakan format: /lang id atau /lang en")

        user_lang[message.chat.id] = args[1]
        bahasa = "Bahasa Indonesia" if args[1] == "id" else "English"
        bot.reply_to(message, f"✅ Bahasa jawaban diubah ke: {bahasa}")

    @bot.message_handler(commands=['ask'])
    def handle_ask(message):
        query = message.text.replace("/ask", "", 1).strip()
        if not query:
            return bot.reply_to(message, "❗ Gunakan format: /ask ")

        bot.reply_to(message, "⏳ Sedang memikirkan jawaban...")

        lang = user_lang.get(message.chat.id, "id") #default: id
        answer = ask_gpt(query, lang)
        bot.send_message(message.chat.id, answer)

