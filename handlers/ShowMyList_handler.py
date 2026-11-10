import os
from dotenv import load_dotenv
import psycopg2
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters,
)

#load the database password from the .env file
load_dotenv()
PASSWORD = os.getenv("DATABASE_PASSWORD")


#show the user wishlist from the database
async def show_my_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            dbname='telegram_db',
            user='postgres',
            password=PASSWORD,
            host='127.0.0.1',
            port='5432',
        )

        cursor = connection.cursor()

        await update.message.reply_text('Подключенно к БД')
    except Exception as error:
        await update.message.reply_text(f'Ошибка при подключении к базе данных: {error}')
        return