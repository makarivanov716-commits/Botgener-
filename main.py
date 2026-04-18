import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🔥 База шаблонов (можешь расширять)
TEMPLATES = [
    "🔥 {topic} — уже здесь\n\n💥 Не упусти шанс\n👉 Пиши прямо сейчас",
    "⚡️ {topic}\n\n🚀 Доступ открыт\n📩 Жми и смотри",
    "💣 {topic}\n\n🔞 Только для своих\n👉 Успей зайти",
    "👀 {topic}\n\n💎 Лучшее уже внутри\n📲 Напиши мне",
]

TOPICS = [
    "ГОРЯЧИЕ ВИДЕО",
    "НОВЫЙ КОНТЕНТ",
    "ЭКСКЛЮЗИВ",
    "ТОП ПОДБОРКА",
    "ЗАКРЫТЫЙ ДОСТУП"
]

# 🎯 Генерация текста
def generate_text():
    template = random.choice(TEMPLATES)
    topic = random.choice(TOPICS)
    return template.format(topic=topic)

# ▶️ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Бот готов.\n\nЖми /gen чтобы получить текст"
    await update.message.reply_text(text)

# 🔥 /gen — генерация
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = generate_text()
    await update.message.reply_text(text)

# 🚀 запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main() 