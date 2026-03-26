import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
from aiogram.filters import CommandStart

BOT_TOKEN = "8572454769:AAGLqkS2l62r29oLMRYQ6KBfUxsgAdxv1sI"
ADMIN_ID = 8508142416  # O'z ID raqamingizni yozing
WEBAPP_URL = "https://sizning-github-nomingiz.github.io/papka-nomi/" # Buni GitHub'dan olgach o'zgartiramiz

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Bazani yaratish
conn = sqlite3.connect('ombor.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, status TEXT)')
conn.commit()

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    cur.execute("SELECT status FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    if user is None:
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔐 Admindan ruxsat so'rash", callback_data="ruxsat_sorash")]
        ])
        await message.answer("Tizimga kirish uchun ruxsat so'rang.", reply_markup=btn)
    elif user[0] == "pending":
        await message.answer("Kuting, admin hali tasdiqlamadi.")
    elif user[0] == "approved":
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 Omborga kirish", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        await message.answer("Tizimga xush kelibsiz!", reply_markup=btn)

@dp.callback_query(F.data == "ruxsat_sorash")
async def sorov_yuborish(call: CallbackQuery):
    user_id = call.from_user.id
    cur.execute("INSERT OR IGNORE INTO users (id, status) VALUES (?, ?)", (user_id, "pending"))
    conn.commit()
    await call.message.edit_text("So'rov adminga yuborildi.")

    # Adminga xabar
    admin_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qabul", callback_data=f"qabul_{user_id}"),
         InlineKeyboardButton(text="❌ Rad", callback_data=f"rad_{user_id}")]
    ])
    await bot.send_message(ADMIN_ID, f"Yangi so'rov:\nID: {user_id}\nIsmi: {call.from_user.first_name}", reply_markup=admin_btn)

@dp.callback_query(F.data.startswith("qabul_"))
async def qabul_qilish(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    cur.execute("UPDATE users SET status = 'approved' WHERE id = ?", (user_id,))
    conn.commit()
    await call.message.edit_text("Foydalanuvchi qabul qilindi.")
    await bot.send_message(user_id, "Admin sizga ruxsat berdi! /start ni bosing.")

async def main():
    print("Bot ishlayapti...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
