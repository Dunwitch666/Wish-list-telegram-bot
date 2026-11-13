#libraries import
from html import escape
from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest

CAPTION_LIMIT = 1024   #Telegram limit for photo caption
MESSAGE_LIMIT = 4096   #Telegram limit for text message


def format_gift(number: int, label: str) -> str:
    return f"🎁 <b>{number}.</b> {escape(label)}"


async def _send_text_chunks(update: Update, lines: list[str]) -> None:
    message = update.effective_message
    chunk = ""
    for line in lines:
        if chunk and len(chunk) + len(line) + 2 > MESSAGE_LIMIT:
            await message.reply_text(chunk, parse_mode=ParseMode.HTML)
            chunk = ""
        chunk = f"{chunk}\n\n{line}" if chunk else line
    if chunk:
        await message.reply_text(chunk, parse_mode=ParseMode.HTML)


#send the wishlist to the user, with proper formatting and handling of gifts with images
async def send_wishlist(update: Update, gifts: list[tuple], title: str, empty_text: str) -> None:
    message = update.effective_message

    if not gifts:
        await message.reply_text(empty_text)
        return

    await message.reply_text(
        f"✨ <b>{escape(title)}</b> ({len(gifts)})",
        parse_mode=ParseMode.HTML,
    )

    text_buffer: list[str] = []  
    for number, (label, image_file_id) in enumerate(gifts, start=1):
        text = format_gift(number, label)

        if not image_file_id:
            text_buffer.append(text)
            continue

        await _send_text_chunks(update, text_buffer)
        text_buffer = []

        try:
            if len(text) <= CAPTION_LIMIT:
                await message.reply_photo(
                    photo=image_file_id, caption=text, parse_mode=ParseMode.HTML
                )
            else:
                await message.reply_photo(photo=image_file_id)
                await _send_text_chunks(update, [text])
        except BadRequest:
            await _send_text_chunks(update, [text + "\n<i>(картинку не удалось загрузить)</i>"])

    await _send_text_chunks(update, text_buffer)