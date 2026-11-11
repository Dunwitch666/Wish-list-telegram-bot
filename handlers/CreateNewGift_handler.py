from contextlib import closing

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from db import get_connection
from main import register_user

TEXT, PHOTO = range(2)

async def post_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    register_user(update)
    await update.message.reply_text("Введите текст вашего подарка: название, описание, цену, ссылку на товар, если пожелаете.",)
    return TEXT

async def post_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Если хотите, отправте картинку")
    return PHOTO