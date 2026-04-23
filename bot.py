import telebot

BOT_TOKEN = "8763718986:AAFaVGHQe-QiG1waO24-ZH5jY4-t9FcRWnA"

import telebot
import os
import base64
from openai import OpenAI

# TOKENS
BOT_TOKEN = os.getenv("8763718986:AAFaVGHQe-QiG1waO24-ZH5jY4-t9FcRWnA")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)


# START
@bot.message_handler(commands=['start'])
def start(message):
    text = """Assalomu alaykum 😊

TOGO GROUP PRO ga xush kelibsiz!

Qaysi xizmat kerak? 👇
1️⃣ Abyomni bukva
2️⃣ Banner
3️⃣ Stend
4️⃣ Dizayn
5️⃣ Poligrafiya
6️⃣ Boshqa savol
"""
    bot.send_message(message.chat.id, text)


# TEXT HANDLER
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle(message):
    user = message.text.lower()

    if user == "1" or "bukva" in user:
        bot.send_message(message.chat.id, """Abyomni bukva narxi:

💰 1 sm = 9000 so'm

Masalan:
40 sm = 360 000 so'm
50 sm = 450 000 so'm

Nechta harf va o'lchamini yozing 👇""")

    elif user == "2" or "banner" in user:
        bot.send_message(message.chat.id, """Banner narxi:

💰 1 m² = 35 000 so'm

Banner + karkas:
60 000 – 90 000 so'm / m²

O'lchamini yozing (masalan: 2x3) 👇""")

    elif user == "3":
        bot.send_message(message.chat.id, "Stend haqida ma'lumot beramiz. O'lcham yozing 👇")

    elif user == "4":
        bot.send_message(message.chat.id, "Qanday dizayn kerak? Minimal / Premium 👇")

    elif user == "5":
        bot.send_message(message.chat.id, "Poligrafiya xizmatlari mavjud. Nima kerak? 👇")

    else:
        bot.send_message(message.chat.id, """Savolingizni yozing 😊

📦 Buyurtma uchun:
Ism + Telefon + Manzil qoldiring""")


# 📸 IMAGE + AI ANALYSIS
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "⏳ Rasmni analiz qilyapman...")

    try:
        # Telegramdan rasm olish
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # base64 ga o‘tkazish
        image_base64 = base64.b64encode(downloaded_file).decode("utf-8")

        # OpenAI ga yuborish
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Bu rasmda nima bor? Agar reklama yoki dizayn bo‘lsa, qisqa qilib tushuntir."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )

        answer = response.choices[0].message.content

        bot.send_message(message.chat.id, f"📸 Natija:\n{answer}")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik:\n{e}")


print("Bot ishga tushdi...")
bot.infinity_polling()
bot.polling()
