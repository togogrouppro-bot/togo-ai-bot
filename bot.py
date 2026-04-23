import telebot

BOT_TOKEN = "8763718986:AAFaVGHQe-QiG1waO24-ZH5jY4-t9FcRWnA"

import telebot
import os
import re
from openai import OpenAI

BOT_TOKEN = os.getenv("8763718986:AAFaVGHQe-QiG1waO24-ZH5jY4-t9FcRWnA")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_data = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "👋 Assalomu alaykum!\n\n📸 Rasm yuboring yoki savolingizni yozing")

# 📸 RASM
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

    bot.send_message(message.chat.id, "⏳ Rasmni analiz qilyapman...")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Bu rasmni analiz qil. Bu reklama joyimi? Qanday dizayn qilish mumkin?"},
                {"type": "input_image", "image_url": file_url}
            ]
        }]
    )

    bot.send_message(message.chat.id, response.output_text + "\n\n✍️ Nima yozamiz?")

# 🧠 AI CHAT (tilni o‘zi aniqlaydi)
@bot.message_handler(func=lambda m: True)
def ai_chat(message):
    text = message.text

    # 📞 Telefon aniqlash
    if re.search(r'\+?\d{9,13}', text):
        user_data[message.chat.id] = text

        bot.send_message(message.chat.id, "✅ Rahmat! Tez orada bog‘lanamiz")

        bot.send_message(ADMIN_CHAT_ID,
                         f"🔥 Yangi lead!\n\n👤 ID: {message.chat.id}\n📞 Tel: {text}")
        return

    # 💰 Narx (agar o‘lcham yozsa)
    if re.search(r'\d+\s*sm', text.lower()):
        size = int(re.findall(r'\d+', text)[0])
        price = size * 9000

        bot.send_message(message.chat.id,
                         f"💰 Narx: {price:,} so‘m\n\n📞 Telefoningizni yozing")
        return

    # 🤖 AI javob
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Foydalanuvchiga o‘z tilida javob ber.

Sen reklama kompaniyasi yordamchisisan (TOGO GROUP PRO).

Qisqa, sotuvchi stilida yoz.
Oxirida buyurtmaga yo‘naltir.

Savol: {text}
"""
    )

    bot.send_message(message.chat.id, response.output_text)

print("AI SALES BOT ishlayapti...")
bot.infinity_polling()
bot.polling()
