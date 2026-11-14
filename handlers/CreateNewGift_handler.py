#libraries import
from contextlib import closing
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

#db import
from db import get_connection, register_user

from main import start

TEXT, PHOTO = range(2)

#wirite a text stage
async def post_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    register_user(update)
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await update.message.reply_text("Введите текст вашего подарка: название, описание, цену, ссылку на товар, если пожелаете.", reply_markup=InlineKeyboardMarkup(keyboard))
    return TEXT

#add a photo stage
async def post_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await update.message.reply_text("Если хотите, отправте картинку", reply_markup=InlineKeyboardMarkup(keyboard))
    return PHOTO

#keyboard for canceling the process
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    if query.data == "cancel":
        await query.edit_text(text="Вы нажали: Отмена")
        start(update, context)



#save and request to data
async def save_gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with closing(get_connection()) as conn:
            with conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO gifts (user_id, label, image_file_id) VALUES (%s,%s,%s);"
                )