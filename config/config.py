from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

GROK_API_KEY=os.getenv('GROK_API_KEY')

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}