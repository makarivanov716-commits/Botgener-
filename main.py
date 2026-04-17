import asyncio
import logging
import random
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

# ===== НАСТРОЙКА =====
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===== КНОПКА =====
kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Сгенерировать")]],
    resize_keyboard=True
)

# ===== ЛОГИКА ТЕКСТА =====

symbols = ["~", "*", ":", ".", "•"]
hard_words = ["КАТЕГОРИИ", "ЖАНРЫ"]

def break_word(word):
    if len(word) <= 4:
        return word

    split_pos = random.randint(2, len(word) - 2)

    part1 = word[:split_pos]
    part2 = word[split_pos:]

    if random.random() < 0.6:
        part1 += random.choice(symbols)

    return part1 + "\n" + part2


def style_word(word):
    # сильная ломка для важных слов
    if word in hard_words:
        return break_word(word)

    # обычная ломка
    if random.random() < 0.4:
        return break_word(word)

    # лёгкий стиль
    new_word = ""
    for i, ch in enumerate(word):
        new_word += ch
        if i < len(word) - 1 and random.random() < 0.2:
            new_word += random.choice(symbols)

    return new_word


def generate_text():
    variants = [
        ["ГОРЯЧИЕ", "СПЯЩИЕ"],
        ["ПОДБОРКИ", "ВИДЕО"],
        ["НОВЫЕ", "ВИДЕО"],
        ["КАТЕГОРИИ", "ЖАНРЫ"]
    ]

    chosen = random.sample(variants, 3)

    lines = []

    for pair in chosen:
        styled = [style_word(w) for w in pair]
        lines.append(" ".join(styled))

    endings = ["пиши 🔥", "пиши 😉", "пиши 👀"]

    return "\n\n".join(lines) + "\n\n" + random.choice(endings)


# ===== ХЕНДЛЕРЫ =====

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Жми кнопку 👇", reply_markup=kb)


@dp.message(F.text == "🎲 Сгенерировать")
async def generate(message: Message):
    text = generate_text()
    await message.answer(text)


# ===== ЗАПУСК =====

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
