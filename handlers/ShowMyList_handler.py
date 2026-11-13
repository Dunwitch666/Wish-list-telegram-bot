#libraries import
from contextlib import closing
from telegram import Update
from telegram.ext import ContextTypes

#import db
from db import get_connection

#import send list function
from wishlist_view import send_wishlist


#request to data to select the personal user wishlist
def fetch_gifts(user_id: int) -> list[tuple]:
    with closing(get_connection()) as conn:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT label, image_file_id FROM gifts "
                "WHERE user_id = %s ORDER BY created_at, id;",
                (user_id,),
            )
            return cur.fetchall()


#send wish list from data
async def show_my_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    gifts = fetch_gifts(update.effective_user.id)
    await send_wishlist(
        update,
        gifts,
        title="Твой вишлист",
        empty_text="Твой вишлист пока пуст. Нажми «Создать подарок», чтобы добавить первое желание 🎀",
    )