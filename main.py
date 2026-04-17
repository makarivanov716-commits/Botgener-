import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# кнопка
kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Сгенерировать")]],
    resize_keyboard=True
)

# слова
STRONG_WORDS = ["мамки", "спящие", "мелкие", "возраста", "жанры", "контент"]

BASE_TEXTS = [
    "мамки спящие мелкие и другие горячие жанры все возраста",
    "мамки мелкие спящие и другой сочный контент все возраста",
    "разные жанры мамки спящие мелкие и многое другое",
    "горячие жанры мамки мелкие спящие и другие форматы",
    "мамки спящие и мелкие разные возраста и другие жанры"
]

SYMBOLS = ["•", ".", "/", "~", "*", ";", ":", "|"]
EMOJIS = ["🔥", "💯", "🥰", "🔞", "❗️", "❤️"]

# 🔥 шифровка слова
def corrupt_word(word, strong=False):
    result = ""

    for ch in word:
        result += ch

        if strong:
            if random.random() < 0.6:
                result += random.choice(SYMBOLS)
        else:
            if random.random() < 0.25:
                result += random.choice(SYMBOLS)

    # разрыв слова (как у тебя)
    if strong and random.random() < 0.5 and len(result) > 4:
        cut = len(result) // 2
        result = result[:cut] + " " * random.randint(5, 15) + result[cut:]

    return result

# 🔥 обработка текста
def style_text(text):
    words = text.split()
    result = []

    for w in words:
        clean = w.lower()

        if clean in STRONG_WORDS:
            result.append(corrupt_word(w, True))
        else:
            result.append(corrupt_word(w, False))

    text = " ".join(result)

    # строки как у тебя
    parts = text.split(" ")
    lines = []
    i = 0

    while i < len(parts):
        chunk = parts[i:i+random.randint(2,4)]
        i += len(chunk)

        line = " ".join(chunk)

        # разнос
        if random.random() < 0.6 and len(chunk) >= 2:
            left = chunk[0]
            right = " ".join(chunk[1:])
            space = " " * random.randint(5, 20)
            line = left + space + right

        # иногда капс
        if random.random() < 0.4:
            line = line.upper()

        lines.append(line)

        if random.random() < 0.3:
            lines.append("")

    final = "\n".join(lines)

    final += "\n\n" + random.choice([
        f"ПИШИ {random.choice(EMOJIS)}",
        f"ПИШИ В ЛС {random.choice(EMOJIS)}",
        f"ЖМИ {random.choice(EMOJIS)}"
    ])

    return final

# генерация
def generate_text():
    base = random.choice(BASE_TEXTS)
    return style_text(base)

# старт
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Жми кнопку 👇", reply_markup=kb)

# обработка
@dp.message()
async def handler(message: Message):
    if "ген" in message.text.lower():
        await message.answer(generate_text(), reply_markup=kb)

# запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
