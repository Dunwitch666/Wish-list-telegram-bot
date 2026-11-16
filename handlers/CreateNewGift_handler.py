#libraries import
from contextlib import closing
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

#db import
from db import get_connection, register_user

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
    context.user_data["label"] = update.message.text   # запоминаем текст до сохранения
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    await update.message.reply_text("Теперь отправьте картинку (как фото)", reply_markup=InlineKeyboardMarkup(keyboard))
    return PHOTO

#if the user sent something that is not a photo
async def wrong_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Нужна картинка. Отправьте её как фото или нажмите «Отмена».")
    return PHOTO

#keyboard for canceling the process
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    context.user_data.pop("label", None)
    await query.edit_message_text(text="Создание подарка отменено.")
    return ConversationHandler.END

#save and request to data
async def save_gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    label = context.user_data.pop("label")
    file_id = update.message.photo[-1].file_id   # последний элемент = лучшее качество

    with closing(get_connection()) as conn:
            with conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO gifts (user_id, label, image_file_id) VALUES (%s,%s,%s);",
                    (update.effective_user.id, label, file_id),
                )

    await update.message.reply_text("Подарок добавлен 🎁")
    return ConversationHandler.END

#dialog assembly
create_gift_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Создать подарок$"), post_text)],
    states={
        TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, post_image)],
        PHOTO: [
            MessageHandler(filters.PHOTO, save_gift),
            MessageHandler(~filters.PHOTO & ~filters.COMMAND, wrong_photo),
        ],
    },
    fallbacks=[CallbackQueryHandler(button_handler, pattern="^cancel$")],
)