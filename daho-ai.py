import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction
import asyncio

TOKEN = "8495577934:AAHpF1ovCvcT3ywq9b00dvPIfwd51yKTeqQ"
CHANNEL_ID = "@muhammadsiddiqdev"

bot = Bot(token=TOKEN)
dp = Dispatcher()


def check_member(user_id: int) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    r = requests.get(url, params={"chat_id": CHANNEL_ID, "user_id": user_id}).json()
    status = r.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    if check_member(message.from_user.id):
        await message.answer("Assalomu alaykum! Botga xush kelibsiz!")
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID[1:]}")]
        ])
        await message.answer("Iltimos, kanalga obuna bo‘ling!", reply_markup=kb)


@dp.message(F.text)
async def echo(message: types.Message):
    if not check_member(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_ID[1:]}")]
        ])
        await message.answer("Iltimos, kanalga obuna bo‘ling!", reply_markup=kb)
        return

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        r = requests.get(
    "https://maebotchatai.onrender.com/chat",
    params={"savol": message.text},  
    timeout=15
)

        r.raise_for_status()

        try:
            j = r.json()
            s = j.get('answer') or j.get('text') or j.get('response') or str(j)
        except ValueError:
            s = r.text

        for i in range(0, len(s), 4096):
            await message.answer(s[i:i + 4096])

    except requests.RequestException:
        await message.answer("API bilan bog‘lanishda xatolik yuz berdi!")

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def main():
    keep_alive()
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot ishga tushdi...✅")
    asyncio.run(main())
