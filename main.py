import os
import time
import threading
import requests as http
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask, request, jsonify
from flask_cors import CORS

BOT_TOKEN  = "8572454769:AAGLqkS2l62r29oLMRYQ6KBfUxsgAdxv1sI"
ADMIN_ID   = 8508142416
PORT       = int(os.getenv("PORT", 10000))
WEBAPP_URL = "https://grandelectronics779-commits.github.io/yangi-bot-ombori-/"
FB_URL     = "https://scholaris-ai-default-rtdb.firebaseio.com"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
CORS(app)

# ── Firebase yozish (REST API) ──────────────────────────────────────────────
def fb_set(path, data):
    try: http.put(f"{FB_URL}/{path}.json", json=data, timeout=5)
    except: pass

def fb_update(path, data):
    try: http.patch(f"{FB_URL}/{path}.json", json=data, timeout=5)
    except: pass

# ── Flask endpointlar ───────────────────────────────────────────────────────
@app.route("/")
def home():
    return "Gelectronics Cloud Bot ishlayapti! ✅", 200

@app.route("/api/request_access", methods=["POST"])
def request_access():
    d = request.json
    uid      = d.get("user_id")
    name     = d.get("name", "Noma'lum")
    username = d.get("username", "")

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Ruxsat berish", callback_data=f"av_{uid}"),
        InlineKeyboardButton("❌ Rad etish",     callback_data=f"rv_{uid}")
    )
    text = (
        f"🔔 <b>Omborxonaga kirish so'rovi</b>\n\n"
        f"👤 Ism: <b>{name}</b>\n"
        f"🆔 ID: <code>{uid}</code>\n"
        f"📱 Username: @{username}\n\n"
        f"📋 Sabab: <i>Omborxonani ko'rish uchun</i>"
    )
    bot.send_message(ADMIN_ID, text, parse_mode="HTML", reply_markup=markup)
    return jsonify({"status": "ok"})

@app.route("/api/request_edit", methods=["POST"])
def request_edit():
    d = request.json
    uid      = d.get("user_id")
    name     = d.get("name", "Noma'lum")
    username = d.get("username", "")
    action   = d.get("action", "")

    action_text = {"add": "➕ Mahsulot qo'shish",
                   "edit": "✏️ Tahrirlash",
                   "delete": "🗑 O'chirish"}.get(action, action)

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Ruxsat", callback_data=f"ae_{uid}"),
        InlineKeyboardButton("❌ Rad",    callback_data=f"re_{uid}")
    )
    text = (
        f"✏️ <b>Tahrirlash so'rovi</b>\n\n"
        f"👤 Ism: <b>{name}</b>\n"
        f"🆔 ID: <code>{uid}</code>\n"
        f"📱 Username: @{username}\n\n"
        f"📋 Amal: <b>{action_text}</b>"
    )
    bot.send_message(ADMIN_ID, text, parse_mode="HTML", reply_markup=markup)
    return jsonify({"status": "ok"})

# ── Callback tugmalar ───────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    d = call.data

    if d.startswith("av_"):       # approve view
        uid = int(d[3:])
        fb_update(f"devices/{uid}", {"viewPerm": True, "editPerm": False, "status": "approved"})
        bot.answer_callback_query(call.id, "✅ Ruxsat berildi!")
        try:
            bot.edit_message_text(call.message.text + "\n\n✅ RUXSAT BERILDI",
                call.message.chat.id, call.message.message_id, parse_mode="HTML")
        except: pass
        try: bot.send_message(uid, "✅ Omborxonaga kirish ruxsati berildi! Sahifani yoping va qayta oching.")
        except: pass

    elif d.startswith("rv_"):     # reject view
        uid = int(d[3:])
        fb_update(f"devices/{uid}", {"viewPerm": False, "editPerm": False, "status": "rejected"})
        bot.answer_callback_query(call.id, "❌ Rad etildi!")
        try:
            bot.edit_message_text(call.message.text + "\n\n❌ RAD ETILDI",
                call.message.chat.id, call.message.message_id, parse_mode="HTML")
        except: pass
        try: bot.send_message(uid, "❌ Kirishga ruxsat berilmadi.")
        except: pass

    elif d.startswith("ae_"):     # approve edit
        uid = int(d[3:])
        fb_update(f"edit_requests/{uid}", {"status": "approved", "timestamp": int(time.time()*1000)})
        bot.answer_callback_query(call.id, "✅ Tahrirlash ruxsati berildi!")
        try:
            bot.edit_message_text(call.message.text + "\n\n✅ TAHRIRLASH RUXSATI BERILDI",
                call.message.chat.id, call.message.message_id, parse_mode="HTML")
        except: pass
        try: bot.send_message(uid, "✅ Tahrirlash ruxsati berildi! Hozir bajaring.")
        except: pass

    elif d.startswith("re_"):     # reject edit
        uid = int(d[3:])
        fb_update(f"edit_requests/{uid}", {"status": "rejected"})
        bot.answer_callback_query(call.id, "❌ Rad etildi!")
        try:
            bot.edit_message_text(call.message.text + "\n\n❌ RAD ETILDI",
                call.message.chat.id, call.message.message_id, parse_mode="HTML")
        except: pass
        try: bot.send_message(uid, "❌ Tahrirlash ruxsati berilmadi.")
        except: pass

# ── Bot buyruqlari ──────────────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start(msg):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Omborxonani ochish", web_app=WebAppInfo(url=WEBAPP_URL)))
    bot.send_message(msg.chat.id,
        "👋 Salom! <b>Gelectronics Cloud</b> omborxona tizimi.\n\n"
        "⬇️ Quyidagi tugmani bosing:",
        parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def boshqa(msg):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Omborxonani ochish", web_app=WebAppInfo(url=WEBAPP_URL)))
    bot.send_message(msg.chat.id, "👇 Tugmani bosing:", reply_markup=markup)

# ── Ishga tushirish ─────────────────────────────────────────────────────────
def flask_run():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

threading.Thread(target=flask_run, daemon=True).start()
print(f"✅ Server ishga tushdi, port: {PORT}")
print("🤖 Bot polling boshlandi...")
bot.infinity_polling(timeout=30, long_polling_timeout=25)
