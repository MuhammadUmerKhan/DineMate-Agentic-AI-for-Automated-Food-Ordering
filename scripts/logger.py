import logging, os

# Configure logging
logging.basicConfig(
    filename="./logs/foodbot.log",  # Ensure the logs directory exists
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_logger(name):
    """Return a logger instance."""
    return logging.getLogger(name)