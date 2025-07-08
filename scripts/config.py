"""
DineMate Configuration

This module provides core configuration settings and utilities
for the DineMate AI-powered food ordering assistant.

Dependencies:
- os: Path handling and environment variable access
- sqlite3: Database connectivity
- dotenv: Load environment variables from `.env` file
- logger: Custom logging utility
"""

import os, sqlite3
from dotenv import load_dotenv
from scripts.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Static paths
DB_PATH = os.path.join("database", "dinemate.db")
STATIC_CSS_PATH = os.path.join("static", "styles.css")

# Model configuration
DEFAULT_MODEL_NAME = "qwen/qwen3-32b"

def get_db_connection():
    """
    Establish a connection to the DineMate SQLite database.

    Returns:
        sqlite3.Connection: A configured database connection.
    
    Raises:
        sqlite3.Error: If the connection cannot be established.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        logger.info("✅ Database connection established.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"❌ Failed to connect to database: {e}")
        raise
