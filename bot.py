import telebot

BOT_TOKEN = "8763718986:AAFaVGHQe-QiG1waO24-ZH5jY4-t9FcRWnA"

bot = telebot.TeleBot(BOT_TOKEN)

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


# HANDLE
@bot.message_handler(func=lambda message: True)
def handle(message):
    user = message.text.lower()

    # 1 - BUKVA
    if user == "1" or "bukva" in user:
        bot.send_message(message.chat.id, """Abyomni bukva narxi:

💰 1 sm = 9000 so‘m

Masalan:
40 sm = 360 000 so‘m
50 sm = 450 000 so‘m

Nechta harf va o‘lchamini yozing 👇""")


    # 2 - BANNER
    elif user == "2" or "banner" in user:
        bot.send_message(message.chat.id, """Banner narxi:

💰 1 m² = 35 000 so‘m

Banner + karkas:
60 000 – 90 000 so‘m / m²

O‘lchamini yozing (masalan: 2x3) 👇""")


    # 3 - STEND
    elif user == "3" or "stend" in user:
        bot.send_message(message.chat.id, """Stend narxlari:

📌 Karmashka: 25 000 so‘m
📌 Banner stend: 90 000 so‘m/m²
📌 Fomaks: 350 000 so‘m/m²
📌 Alyukabond: 550 000 so‘m/m²

O‘lchamini yozing 👇""")


    # 4 - DIZAYN
    elif user == "4" or "dizayn" in user:
        bot.send_message(message.chat.id, """Qanday dizayn kerak?

1) Minimal
2) Premium
3) Lightbox

Tanlang 👇""")


    # 5 - POLIGRAFIYA
    elif user == "5" or "vizitka" in user or "flayer" in user:
        bot.send_message(message.chat.id, """Poligrafiya xizmatlari:

📌 Vizitka
📌 Flayer
📌 Buklet
📌 Katalog

Nechta dona kerakligini yozing 👇""")


    # 6 - BOSHQA
    else:
        bot.send_message(message.chat.id, """Savolingizni yozing 😊

📩 Buyurtma uchun:
Ism + Telefon + Manzil qoldiring""")
import openai
import os
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", "wb") as f:
        f.write(downloaded_file)

    bot.send_message(message.chat.id, "⏳ Rasmni analiz qilyapman...")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Bu rasmni biznes nuqtai nazardan tushuntir"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + encode_image("image.jpg")
                        }
                    }
                ]
            }
        ]
    )

    bot.send_message(message.chat.id, response['choices'][0]['message']['content'])


bot.polling()
