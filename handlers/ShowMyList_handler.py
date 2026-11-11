import os
from dotenv import load_dotenv
import psycopg2
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters,
)
from contextlib import closing
from db import get_connection

#load the database password from the .env file
load_dotenv()
PASSWORD = os.getenv("DATABASE_PASSWORD")


#show the user wishlist from the database
async def show_my_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass