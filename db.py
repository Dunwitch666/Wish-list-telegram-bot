import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='telegram_db',
        user='postgres',
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5432"),
    )