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
from logger import get_logger

logger = get_logger(__name__)

def prune_messages(left: list, right: list) -> list:
    """Prune old get_full_menu tool messages to reduce token usage."""
    combined = add_messages(left, right)
    # Keep last 10 messages, and exclude old get_full_menu ToolMessages
    filtered = []
    for msg in combined[-10:]:  # Limit to last 10 messages
        if isinstance(msg, dict) and msg.get("type") == "tool" and msg.get("name") == "get_full_menu":
            continue  # Skip old get_full_menu ToolMessages
        filtered.append(msg)
    return filtered

class State(TypedDict):
    messages: Annotated[list, prune_messages]  # Use custom reducer
    menu: dict  # Store menu as a dict, not in messages

    def __init__(self):
        logger.info("🍽️ State initialized")