import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🎲 Сгенерировать")]],
    resize_keyboard=True
)

strong_words = ["мамки", "спящие", "мелкие", "возраста", "жанры", "контент"]
normal_words = ["разные", "горячие", "сочные", "видео", "форматы", "другие"]

symbols = ["•", ".", "~", "*", "/", "|", ";", ":"]

emojis = ["🔥", "💯", "🥵", "❤️", "😈", "❗️"]

# --- шифровка ---
def encrypt(word, strong=False):
    chance = 0.55 if strong else 0.3
    result = ""

    for i, ch in enumerate(word):
        result += ch
        if i != len(word)-1 and random.random() < chance:
            result += random.choice(symbols)

    return result

# --- перенос слова (ВАЖНО: без лишних пустых строк) ---
def split_word(word):
    if len(word) < 6 or random.random() > 0.6:
        return
