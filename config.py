from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()  # Load environment variables from .env

GROK_API_KEY=os.getenv('GROK_API_KEY')

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

DB_PATH = "./foodbot.db"
def get_db_connection():
    """Create and return a database connection to SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ✅ Allows accessing columns by name
    return conn

# print(get_db_connection())