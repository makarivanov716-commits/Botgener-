import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# слова
MAIN_WORDS = ["мамки", "спящие", "мелкие", "контент", "жанры"]
OTHER_WORDS = [
    "горячие", "видео", "разные", "темы", "категории",
    "интересные", "лучшие", "сочные", "новые"
]

EMOJIS = ["🔥", "🥰", "🔞", "💯", "❗️"]

SYMBOLS = ["•", ".", "~", "*", ";", "/", "\\"]

# функция шифровки
def obfuscate(word, strong=False):
    result = ""
    for ch in word:
        if random.random() < (0.5 if strong else 0.25):
            result += random.choice(SYMBOLS)
        result += ch
    return result

# генерация строки
def generate_line(words, strong=False):
    return " ".join([
        obfuscate(w, strong) if w in MAIN_WORDS else obfuscate(w)
        for w in words
    ])

# генерация текста
def generate_text():
    lines = []

    # верх
    lines.append(generate_line([
        random.choice(MAIN_WORDS),
        random.choice(MAIN_WORDS)
    ], strong=True))

    # середина
    lines.append("")
    lines.append(
        generate_line([
            "и", "другие",
            random.choice(OTHER_WORDS),
            random.choice(OTHER_WORDS)
        ])
        + " " + random.choice(EMOJIS)
    )

    lines.append("")
    lines.append(
        generate_line([
            "все",
            "возраста"
        ], strong=True)
        + " " + random.choice(EMOJIS)
    )

    lines.append("")
    lines.append("ПИШИ " + random.choice(EMOJIS))

    return "\n".join(lines)

# старт
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("🎲 Нажми: Сгенерировать")

# генерация
@dp.message()
async def handler(message: Message):
    if "сген" in message.text.lower():
        text = generate_text()
        await message.answer(text)

# запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
