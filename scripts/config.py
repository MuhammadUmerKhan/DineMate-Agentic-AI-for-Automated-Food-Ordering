"""
# DineMate Configuration

This module provides configuration settings for the DineMate foodbot.

## Dependencies
- `os`: For file path handling.
- `sqlite3`: For database connection.
- `dotenv`: For environment variables.
- `logger`: For logging.
"""

import os, sqlite3
from dotenv import load_dotenv
from scripts.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = os.path.join("database", "dinemate.db")
STATIC = os.path.join("static", "styles.css")

def get_db_connection():
    """Create and return a database connection to SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        logger.info("Database connection established")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise