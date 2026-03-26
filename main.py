import os
import telebot
from flask import Flask

# 1. BOT SOZLAMALARI
API_TOKEN = os.getenv('8572454769:AAGLqkS2l62r29oLMRYQ6KBfUxsgAdxv1sI')
bot = telebot.TeleBot(API_TOKEN)

# 2. RENDER UCHUN ODDIY VEB-SERVER (BU PORT MUAMMOSINI HAL QILADI)
server = Flask(__name__)

@server.route("/")
def webhook():
    return "Gelectronics Bot ishlayapti!", 200

# 3. TELEGRAM START BUYRUG'I
@bot.message_handler(commands=['start'])
def start(message):
    # Sizning GitHub Pages manzilingiz
    web_app_url = "https://grandelectronics779-commits.github.io/yangi-bot-ombori-/"
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    web_app = telebot.types.WebAppInfo(web_app_url)
    button = telebot.types.KeyboardButton(text="Gelectronics Cloud 👑", web_app=web_app)
    markup.add(button)
    
    bot.send_message(message.chat.id, "Xush kelibsiz! Omborga kirish uchun tugmani bosing:", reply_markup=markup)

# 4. BOTNI VA SERVERNI BIRGA ISHLATISH
if __name__ == "__main__":
    # Render portni o'zi beradi, biz uni qabul qilamiz
    port = int(os.environ.get("PORT", 5000))
    
    # Botni alohida "oqim"da emas, oddiygina server bilan birga yurgizamiz
    from threading import Thread
    def run_bot():
        bot.infinity_polling()

    Thread(target=run_bot).start()
    server.run(host="0.0.0.0", port=port)
