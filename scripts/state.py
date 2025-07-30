"""
# DineMate State Definition

This module defines the state structure for the DineMate foodbot.

## Dependencies
- `typing`: For type hints.
- `typing_extensions`: For TypedDict.
- `langgraph.graph.message`: For message handling.
- `logger`: For logging.
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from scripts.logger import get_logger

logger = get_logger(__name__)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    menu: dict

    def __init__(self):
        logger.info("🍽️ State initialized")