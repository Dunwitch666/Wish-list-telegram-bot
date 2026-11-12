import os
import psycopg2

#connection with database
def get_connection():
    return psycopg2.connect(
        dbname='telegram_db',
        user='postgres',
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5432"),
    )

#register the user in the database if they are not already registered
def register_user(update: Update) -> None:
    user = update.effective_user
    with closing(get_connection()) as conn:
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (user_id, username) VALUES (%s, %s) "
                "ON CONFLICT (user_id) DO UPDATE SET username = EXCLUDED.username;",
                (user.id, user.username),
            )