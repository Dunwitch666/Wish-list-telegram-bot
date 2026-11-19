#libraries import
from contextlib import closing
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
import hashlib

#import db
from db import get_connection

#define the stages of the conversation
CODE = range(1)

#start closing wishlist flow
async def close_wishlist_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await update.message.reply_text(
        "Введите кодовое слово для закрытия вишлиста:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CODE

#hash the code for security
def hash_data(data: str) -> str:
    combined = f'{data}'.encode('utf-8')
    return hashlib.sha256(combined).hexdigest()


#save wishlist code to database
async def set_wishlist_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    code = update.message.text.strip()
    hash_code = hash_data(code)

    if not code:
        keyboard = [
            [InlineKeyboardButton("Отмена", callback_data="cancel")],
        ]
        await update.message.reply_text(
            "Кодовое слово не может быть пустым. Введите снова:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return CODE

    user_id = update.effective_user.id

    with closing(get_connection()) as conn:
        with conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET wishlist_code = %s WHERE user_id = %s;",
                (hash_code, user_id),
            )

    await update.message.reply_text("Вишлист закрыт кодовым словом 🔒")
    return ConversationHandler.END

#cancel closing flow
async def cancel_close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Закрытие вишлиста отменено.")
    return ConversationHandler.END

#dialog assembly
close_my_list_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Закрыть вишлист$"), close_wishlist_start)],
    states={
        CODE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_wishlist_code),
        ]
    },
    fallbacks=[CallbackQueryHandler(cancel_close, pattern="^cancel$")],
)
