import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# кнопка
kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Сгенерировать")]],
    resize_keyboard=True
)

# слова
strong_words = ["мамки", "спящие", "мелкие", "возраста", "жанры", "контент"]
normal_words = ["разные", "горячие", "сочные", "видео", "форматы", "другие"]

symbols = ["•", ".", "~", "*", "/", "|", ";", ":", "◦"]

emojis = ["🔥", "💯", "🥵", "❤️", "😈", "❗️"]

# мягкая шифровка (читаемая)
def soft_encrypt(word):
    result = ""
    for i, ch in enumerate(word):
        result += ch
        if i != len(word) - 1 and random.random() < 0.3:
            result += random.choice(symbols)
    return result

# сильнее шифровка (но читаемо)
def strong_encrypt(word):
    result = ""
    for i, ch in enumerate(word):
        result += ch
        if i != len(word) - 1 and random.random() < 0.55:
            result += random.choice(symbols)
    return result

# делает перенос с визуальным продолжением
def split_word(word):
    if len(word) < 6 or random.random() > 0.5:
        return word

    cut = random.randint(2, len(word)-2)
    part1 = word[:cut]
    part2 = word[cut:]

    # добавляем визуальное смещение второй строки
    space = " " * random.randint(3, 10)
    return part1 + "\n" + space + part2

def process_word(word, strong=False):
    if strong:
        w = strong_encrypt(word)
    else:
        w = soft_encrypt(word)

    return split_word(w)

def generate_text():
    try:
        # выбираем слова
        w1 = process_word(random.choice(strong_words), True)
        w2 = process_word(random.choice(strong_words), True)
        w3 = process_word(random.choice(strong_words), True)

        n1 = process_word(random.choice(normal_words))
        n2 = process_word(random.choice(normal_words))

        emoji = random.choice(emojis)

        upper = random.random() < 0.5

        if upper:
            text = f"""
{w1.upper()}   {w2.upper()}

И ДРУГИЕ {n1.upper()}
        {n2.upper()} {emoji}

ВСЕ {w3.upper()} {random.choice(emojis)}

ПИШИ {random.choice(emojis)}
"""
        else:
            text = f"""
{w1}   {w2}

и другие {n1}
        {n2} {emoji}

все {w3} {random.choice(emojis)}

пиши {random.choice(emojis)}
"""

        # чистим лишние переносы
        text = "\n".join([line.rstrip() for line in text.split("\n") if line.strip() != ""])

        return text

    except Exception as e:
        print(e)
        return "Ошибка генерации 😢"

@dp.message()
async def handler(message: types.Message):
    if message.text.lower() in ["/start", "старт"]:
        await message.answer("Жми кнопку 👇", reply_markup=kb)
        return

    if message.text == "🎲 Сгенерировать":
        text = generate_text()
        await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
