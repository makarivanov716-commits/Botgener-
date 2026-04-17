import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os

# ====== НАСТРОЙКИ ======
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ====== КНОПКА ======
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("🎲 Сгенерировать"))

# ====== СЛОВА ======
strong_words = [
    "мамки", "спящие", "мелкие", "контент", "жанры"
]

other_words = [
    "разные", "горячие", "новые", "интересные",
    "видео", "темы", "форматы", "подборки"
]

emojis = ["🔥", "💯", "😈", "❤️", "🥵", "😏", "👀", "🤤"]

symbols = [".", "*", "~", ":", ";", "|", "/"]

# ====== ШИФРОВКА ======
def obfuscate(word, strong=False):
    result = ""

    for i, char in enumerate(word):
        result += char

        if i != len(word) - 1:
            if strong:
                if random.random() < 0.8:
                    result += random.choice(symbols)
            else:
                if random.random() < 0.3:
                    result += random.choice(symbols)

    return result

# ====== РАЗБИЕНИЕ СЛОВ (БЕЗ ЛОМА ЧИТАЕМОСТИ) ======
def split_word(word):
    if len(word) < 6 or random.random() < 0.6:
        return [word]

    cut = random.randint(2, len(word)-2)
    return [word[:cut], word[cut:]]

# ====== СБОРКА СТРОК ======
def build_line(words):
    line_parts = []

    for w in words:
        if w in strong_words:
            w = obfuscate(w, True)
        else:
            w = obfuscate(w, False)

        parts = split_word(w)

        for i, p in enumerate(parts):
            if i > 0:
                line_parts.append(p)
            else:
                line_parts.append(p)

    return " ".join(line_parts)

# ====== ГЕНЕРАЦИЯ ======
def generate_text():
    try:
        lines = []

        # иногда капс
        use_caps = random.choice([True, False])

        # строка 1
        line1_words = random.sample(strong_words, 2)
        line1 = build_line(line1_words)

        # строка 2
        line2_words = random.sample(other_words, 3)
        line2 = build_line(line2_words)

        # строка 3
        line3_words = ["и"] + random.sample(other_words, 2)
        line3 = build_line(line3_words)

        # строка 4
        line4 = "пиши " + random.choice(emojis)

        lines = [line1, line2, line3, line4]

        # капс иногда
        if use_caps:
            lines = [l.upper() for l in lines]

        # нормальные отступы
        text = f"{lines[0]}\n\n{lines[1]}\n{lines[2]}\n\n{lines[3]}"

        return text

    except Exception as e:
        print("GEN ERROR:", e)
        return "Ошибка генерации ⚠️"

# ====== ХЕНДЛЕРЫ ======
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🎲 Нажми кнопку для генерации", reply_markup=kb)

@dp.message_handler(lambda message: message.text == "🎲 Сгенерировать")
async def generate(message: types.Message):
    try:
        text = generate_text()
        await message.answer(text)
    except Exception as e:
        print("ERROR:", e)
        await message.answer("⚠️ Ошибка")

# ====== ЗАПУСК ======
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
