"""
# DineMate State Definition

This module defines the state structure for the DineMate foodbot using LangGraph's TypedDict
and annotated types. The state holds messages, current order details, and the menu.

## Dependencies
- `typing`: For type hints.
- `typing_extensions`: For TypedDict.
- `langgraph.graph.message`: For message handling.
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    order: str
    menu: dict