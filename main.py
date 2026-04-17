import asyncio
import os
import random

from aiogram import Bot, Dispatcher, types
import openai

# ключи
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate_text():
    prompt = """
Сгенерируй РУССКИЙ рекламный текст как в Telegram.

Стиль:
- хаотичные переносы строк
- разные символы: • ; / \\ ~ | *
- слова иногда ломаются
- эмодзи: 🔥🥰🔞💯❗️

ВАЖНО:
Слова "мамки", "спящие", "мелкие", "жанры", "контент"
делай БОЛЕЕ зашифрованными чем остальные,
но чтобы их можно было прочитать.

Текст должен выглядеть живым, не шаблонным.
Каждый раз новый.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.3
    )

    return response.choices[0].message.content


@dp.message()
async def handler(message: types.Message):
    text = generate_text()
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
