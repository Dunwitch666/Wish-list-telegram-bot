import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
            ["Мой вишлист", "Создать подарок", "Удалить подарок"],
            ["Закрыть вишлист", "Вишлист друзей"],
        ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Чем займемся сегодня?", reply_markup=markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "Мой вишлист":
        await update.message.reply_text("Это ваш вишлист.")
    elif text == "Создать подарок":
        await update.message.reply_text("Создание подарка.")
    elif text == "Удалить подарок":
        await update.message.reply_text("Удаление подарка.")
    elif text == "Закрыть вишлист":
        await update.message.reply_text("Вишлист закрыт.")
    elif text == "Вишлист друзей":
        await update.message.reply_text("Это вишлист ваших друзей.")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
