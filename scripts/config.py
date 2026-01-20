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
from pathlib import Path
from pydantic import SecretStr
from scripts.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Environment variables
GROQ_API_KEY = SecretStr(os.getenv("GROQ_API_KEY") or "")

# Temperature for LLM responses
TEMPERATURE = os.getenv("TEMPERATURE", 0.5)

# Static paths
DB_PATH = Path(__file__).parent.parent / "database" / "dinemate.db"
STATIC_CSS_PATH =  Path(__file__).parent.parent / "static" / "styles.css"

# langsmith configuration
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "DineMate")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_API_KEY = SecretStr(os.getenv("LANGSMITH_API_KEY") or "")

# Short term memory handling
SUMMARY_MESSAGE_THRESHOLD = 15          # trigger summary after this many messages
KEEP_LAST_MESSAGES = 4                  # always keep last N messages verbatim

# Model configuration
DEFAULT_MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", 'openai/gpt-oss-120b')
MODEL_NAME = os.getenv("MODEL_NAME", "qwen/qwen3-32b")

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
        logger.info("✅ Database connected")
        return conn
    except sqlite3.Error as e:
        logger.error({"error": str(e), "message": "❌ Connection failed"})
        raise