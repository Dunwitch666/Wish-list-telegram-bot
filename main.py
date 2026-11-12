import os
from dotenv import load_dotenv
import psycopg2
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters,
)
from contextlib import closing
from db import get_connection, register_user

from handlers.ShowMyList_handler import show_my_list
from handlers.CreateNewGift_handler import create_gift

#load the token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

#handle the /start command and send a welcome message with a keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    register_user(update)

    keyboard = [
        ["Мой вишлист", "Создать подарок", "Удалить подарок"],
        ["Закрыть вишлист", "Вишлист друзей"],
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(f"Привет {user.first_name}! Чем займемся сегодня?", reply_markup=markup)

#handle the text messages from the user and respond accordingly
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "Мой вишлист":
        await show_my_list(update, context)
    elif text == "Создать подарок":
        await create_gift(update, context)
    elif text == "Удалить подарок":
        await update.message.reply_text("Удаление подарка.")
    elif text == "Закрыть вишлист":
        await update.message.reply_text("Вишлист закрыт.")
    elif text == "Вишлист друзей":
        await update.message.reply_text("Это вишлист ваших друзей.")

#main function to run the bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
