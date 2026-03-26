import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

BOT_TOKEN = os.getenv('8572454769:AAGLqkS2l62r29oLMRYQ6KBfUxsgAdxv1sI')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Render'da Environment Variables qismiga tokenni qo'shganingizni tekshiring.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start buyrug'i bosilganda HAMMAGA Web App tugmasi (URL) chiqishi shart!
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Dasturga kirish manzili (Haqiqiy himoya shu linkning ichida ishlaydi)
    web_app_url = "https://grandelectronics779-commits.github.io/yangi-bot-ombori-/" 
    
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Gelectronics Cloud 👑", web_app=WebAppInfo(url=web_app_url))]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Assalomu alaykum!\n\n"
        "Gelectronics omboriga xush kelibsiz. Pastdagi tugmani bosib tizimga kiring:", 
        reply_markup=markup
    )

# Render "Port scan timeout" deb xato bermasligi uchun mitti soxta veb-server
async def handle_ping(request):
    return web.Response(text="Gelectronics Bot 100% ishlayapti va himoyalangan!")

async def main():
    # 1. Soxta veb-serverni sozlash va ishga tushirish
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render o'zi bergan portni topamiz, yo'q bo'lsa 10000 ishlatamiz
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Veb-server {port}-portda ishga tushdi...")

    # 2. Telegram botni ishga tushirish
    print("Telegram bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
