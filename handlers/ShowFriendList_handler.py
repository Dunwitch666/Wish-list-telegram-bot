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

#import db
from db import get_connection

#import show list function
from wishlist_view import send_wishlist
from handlers.ShowMyList_handler import fetch_gifts

#define the stages of the conversation
USERNAME, CODE = range(2)

#start friend wishlist search
async def show_friend_list_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await update.message.reply_text(
        "Введите username друга (без @):",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return USERNAME

#search user by username
async def find_friend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    username = update.message.text.strip().lstrip("@")

    if not username:
        await update.message.reply_text("Пожалуйста, введите username.")
        return USERNAME

    with closing(get_connection()) as conn:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, wishlist_code FROM users WHERE username = %s;",
                (username,),
            )
            row = cur.fetchone()

    if not row:
        keyboard = [
                [InlineKeyboardButton("Отмена", callback_data="cancel")],
        ]
        await update.message.reply_text("Пользователь с таким username не найден. Попробуйте снова:", reply_markup=InlineKeyboardMarkup(keyboard))
        return USERNAME

    friend_id, wishlist_code = row

    # save friend_id for later steps
    context.user_data["friend_id"] = friend_id

    if not wishlist_code:
        # wishlist is open — show directly
        return await send_friend_wishlist(update, context)

    # wishlist is closed — ask for code
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await update.message.reply_text(
        "Вишлист этого пользователя закрыт кодовым словом. Введите код:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CODE

#show friend's wishlist
async def send_friend_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    friend_id = context.user_data.get("friend_id")
    if not friend_id:
        await update.message.reply_text("Ошибка: пользователь не найден.")
        return ConversationHandler.END

    gifts = fetch_gifts(friend_id)

    await send_wishlist(
        update,
        gifts,
        title="Вишлист друга",
        empty_text="У этого пользователя пустой вишлист.",
    )

    return ConversationHandler.END

#check code word
async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    code = update.message.text.strip()
    friend_id = context.user_data.get("friend_id")

    if not friend_id:
        await update.message.reply_text("Ошибка: пользователь не найден.")
        return ConversationHandler.END

    with closing(get_connection()) as conn:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT wishlist_code FROM users WHERE user_id = %s;",
                (friend_id,),
            )
            row = cur.fetchone()

    if not row or row[0] != code:
        await update.message.reply_text("Неверное кодовое слово. Попробуйте снова:")
        return CODE

    await send_friend_wishlist(update, context)
    return ConversationHandler.END

#cancel closing flow
async def cancel_friend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Поиск вишлиста отменён.")
    return ConversationHandler.END

#dialog assembly
show_friend_list_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Вишлист друзей$"), show_friend_list_start)],
    states={
        USERNAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, find_friend),
        ],
        CODE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, check_code),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel_friend, pattern="^cancel$")],
)
