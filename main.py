import asyncio
import random
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Сгенерировать")]],
    resize_keyboard=True
)

print("БОТ СТАРТАНУЛ")

def generate_text():
    return "ТЕСТ РАБОТАЕТ"

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Жми кнопку 👇", reply_markup=kb)

@dp.message(F.text == "🎲 Сгенерировать")
async def generate(message: Message):
    await message.answer(generate_text())

async def main():
    print("POLLING START")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())