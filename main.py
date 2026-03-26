import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask

# ---------- TOKEN VA PORT ----------
BOT_TOKEN  = os.getenv("8572454769:AAGLqkS2l62r29oLMRYQ6KBfUxsgAdxv1sI")
PORT       = int(os.getenv("PORT", 10000))
WEBAPP_URL = "https://grandelectronics779-commits.github.io/yangi-bot-ombori-/"

bot = telebot.TeleBot(BOT_TOKEN)

# ---------- FLASK (Render uchun) ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot ishlayapti!", 200

def flask_thread():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

# ---------- TUGMA ----------
def tugma():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Omborxonani ochish", web_app=WebAppInfo(url=WEBAPP_URL)))
    return markup

# ---------- BOT BUYRUQLARI ----------
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id,
        "👋 Salom! Omborxonani boshqarish uchun quyidagi tugmani bosing:",
        reply_markup=tugma())

@bot.message_handler(func=lambda m: True)
def boshqa(msg):
    bot.send_message(msg.chat.id, "👇 Tugmani bosing:", reply_markup=tugma())

# ---------- ISHGA TUSHIRISH ----------
threading.Thread(target=flask_thread, daemon=True).start()
print("✅ Server ishga tushdi, port:", PORT)

bot.infinity_polling(timeout=30, long_polling_timeout=25)
