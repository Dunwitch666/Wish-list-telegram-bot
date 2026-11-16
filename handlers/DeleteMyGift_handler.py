#libraries import
from contextlib import closing
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)

#import db
from db import get_connection

#import show my list
from handlers.ShowMyList_handler import show_my_list

#define the stages of the conversation
ID = range(1)

#choose id message
async def id_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
            [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await show_my_list(update, context)
    await update.message.reply_text("Введите id подарка для удаления:", reply_markup=InlineKeyboardMarkup(keyboard))
    return ID

#delete the gift
async def delete_gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
                [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    gift_id_text = update.message.text.strip()
    if not gift_id_text.isdigit():
        await update.message.reply_text("Пожалуйста, введите числовой id подарка.",  reply_markup=InlineKeyboardMarkup(keyboard))
        return ID

    gift_id = int(gift_id_text)
    user_id = update.effective_user.id

    with closing(get_connection()) as conn:
        with conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM gifts WHERE id = %s AND user_id = %s;",
                (gift_id, user_id),
            )
            deleted = cur.rowcount

    if deleted:
        await update.message.reply_text("Подарок удалён 🗑️")
    else:
        await update.message.reply_text("Подарок с таким id не найден или не принадлежит вам.")

    return ConversationHandler.END

#keyboard for canceling the process
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    context.user_data.pop("label", None)
    await query.edit_message_text(text="Удаление подарка отменено.")
    return ConversationHandler.END

#dialog assembly
delete_gift_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Удалить подарок$"), id_choose)],
    states={
        ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_gift)],
    },
    fallbacks=[CallbackQueryHandler(button_handler, pattern="^cancel$")],
)