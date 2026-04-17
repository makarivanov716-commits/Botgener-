import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
import random

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

symbols = ["•", ".", "*", "/", "~", ","]
emojis = ["🔥", "🥰", "🔞", "💯", "❗️"]

# словари (расширяй сам)
main_words = ["мамки", "мелкие", "спящие", "разные", "горячие"]
extra_words = ["видео", "жанры", "темы", "контент"]
actions = ["ПИШИ", "ЗАХОДИ", "СМОТРИ"]

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎲 Сгенерировать")],
        [KeyboardButton(text="📦 Блоки"), KeyboardButton(text="🎯 Смешанный")]
    ],
    resize_keyboard=True
)

current_style = "block"


def break_word(word):
    if len(word) < 4:
        return word, ""

    cut = random.randint(1, len(word)-2)
    p1 = word[:cut] + random.choice(symbols)
    p2 = random.choice(symbols) + word[cut:]

    return p1, p2


def line_block():
    w = random.choice(main_words)
    p1, p2 = break_word(w)

    space = " " * random.randint(10, 30)
    return p1 + space + p2


def generate_block():
    text = ""

    # верх
    for _ in range(random.randint(2, 4)):
        text += line_block() + "\n"

    text += "\n"

    # середина
    text += "И ДРУГИЕ " + random.choice(["СОЧ", "ГОРЯЧ", "РАЗН"]) + random.choice(symbols) + "\n"
    text += " " * random.randint(10, 25) + random.choice(symbols) + "НЫЕ " + random.choice(extra_words).upper() + random.choice(emojis) + "\n\n"

    # ещё блок
    if random.random() < 0.7:
        text += "ВСЕ ВО" + random.choice(symbols) + "\n"
        text += " " * random.randint(10, 20) + random.choice(symbols) + "ЗРАСТА" + random.choice(emojis) + "\n\n"

    # конец
    text += random.choice(actions) + random.choice(emojis)

    return text


def generate_mixed():
    text = ""

    # строки
    for _ in range(random.randint(3, 6)):
        w = random.choice(main_words)
        p1, p2 = break_word(w)

        space = " " * random.randint(5, 15)
        text += p1 + space + p2 + "\n"

    text += "\n"

    # рандом фразы
    for _ in range(random.randint(1, 3)):
        text += random.choice(extra_words).upper() + " " + random.choice(main_words) + random.choice(emojis) + "\n"

    text += "\n" + random.choice(actions) + random.choice(emojis)

    return text


def generate_ai_text(style):
    # микс генерации (как нейросеть)
    if style == "mixed":
        if random.random() < 0.5:
            return generate_mixed()
        else:
            return generate_block()
    else:
        if random.random() < 0.7:
            return generate_block()
        else:
            return generate_mixed()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Жми 🎲 — сгенерирую как нейросеть 🔥", reply_markup=kb)


@dp.message()
async def handler(message: types.Message):
    global current_style

    if message.text == "📦 Блоки":
        current_style = "block"
        await message.answer("Стиль: Блоки ✅")

    elif message.text == "🎯 Смешанный":
        current_style = "mixed"
        await message.answer("Стиль: Смешанный ✅")

    elif message.text == "🎲 Сгенерировать":
        result = generate_ai_text(current_style)
        await message.answer(result)

    else:
        await message.answer("Жми 🎲")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
