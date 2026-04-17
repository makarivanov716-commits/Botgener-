import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# НАСТРОЙКИ
# =========================

SYMBOLS = ["*", "•", "~", ":", ";", ".", "|"]

WORDS = [
    "мамки", "спящие", "видео", "подборки",
    "разные", "новые", "темы", "горячие",
    "контент", "интересные", "форматы"
]

ENDINGS = [
    "пиши 🔥",
    "пиши 😉",
    "пиши 👀",
    "жми 🔥",
    "пиши 💬"
]

MODES = {
    "soft": 0.2,
    "medium": 0.4,
    "hard": 0.7
}

user_modes = {}

# =========================
# ГЕНЕРАЦИЯ
# =========================

def corrupt(word, level):
    """ломает слово"""
    result = ""

    for ch in word:
        result += ch
        if random.random() < level:
            result += random.choice(SYMBOLS)

    return result


def split_word(word, level):
    """перенос строки внутри слова"""
    if len(word) < 6 or random.random() > level:
        return word

    i = random.randint(2, len(word) - 2)
    return word[:i] + "\n" + word[i:]


def make_line(words, level, upper=False):
    result = []
    for w in words:
        if upper:
            w = w.upper()

        w = corrupt(w, level)
        w = split_word(w, level)

        result.append(w)

    return " ".join(result)


def generate_text(mode):
    level = MODES.get(mode, 0.4)

    lines = []

    # заголовок
    header = random.sample(WORDS, 2)
    lines.append(make_line(header, level, upper=True))

    # отступ
    lines.append("")

    # основной блок
    for _ in range(random.randint(2, 4)):
        words = random.sample(WORDS, random.randint(2, 3))
        lines.append(make_line(words, level))

    # отступ
    lines.append("")

    # конец
    lines.append(random.choice(ENDINGS))

    return "\n".join(lines)


# =========================
# КНОПКА
# =========================

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Сгенерировать")]],
    resize_keyboard=True
)


# =========================
# КОМАНДЫ
# =========================

@dp.message(Command("start"))
async def start(msg: types.Message):
    user_modes[msg.from_user.id] = "medium"
    await msg.answer("🎯 Режим: medium\nЖми кнопку", reply_markup=kb)


@dp.message(Command("soft"))
async def soft(msg: types.Message):
    user_modes[msg.from_user.id] = "soft"
    await msg.answer("Режим: SOFT")


@dp.message(Command("medium"))
async def medium(msg: types.Message):
    user_modes[msg.from_user.id] = "medium"
    await msg.answer("Режим: MEDIUM")


@dp.message(Command("hard"))
async def hard(msg: types.Message):
    user_modes[msg.from_user.id] = "hard"
    await msg.answer("Режим: HARD 🔥")


# =========================
# ГЕНЕРАЦИЯ
# =========================

@dp.message(lambda msg: msg.text == "🎲 Сгенерировать")
async def gen(msg: types.Message):
    mode = user_modes.get(msg.from_user.id, "medium")
    text = generate_text(mode)
    await msg.answer(text)


# =========================
# СТАРТ
# =========================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
