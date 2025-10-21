import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            filename=os.path.join("logs", "foodbot.log"),
            encoding="utf-8"  # Explicitly set UTF-8 encoding
        ),
        # logging.StreamHandler()  # Optional: Add console output for debugging
    ]
)

def get_logger(name):
    """Return a logger instance with UTF-8 encoding for emoji support."""
    return logging.getLogger(name)