"""
# DineMate Chatbot Node

This module implements the chatbot node for the DineMate foodbot.

## Dependencies
- `json`: For JSON handling.
- `textwrap`: For formatting prompts.
- `utils`: For LLM configuration.
- `tools`: For get_menu, save_order, and check_status tools.
- `state`: For state definition.
- `logger`: For logging.
"""

import json, textwrap
from scripts.utils import configure_llm
from scripts.tools import get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer
from scripts.state import State
from scripts.config import DEFAULT_MODEL_NAME
from scripts.logger import get_logger

logger = get_logger(__name__)

def chatbot(state: State) -> State:
    """Process user input and interact with the LLM."""
    messages = state["messages"]
    menu = state.get("menu", {})

    if not menu:
        menu = json.loads(get_menu.invoke({}))
        state["menu"] = menu
        logger.info("Cached menu in state")

    system_prompt = textwrap.dedent(f"""
        You are DineMate 🤖🍽️ — a friendly AI food assistant.

        🎯 Your tasks:
        - Understand orders like "2 zingers, 1 fries" and validate from menu: {menu}.
        - Track items in memory and update as needed.
        - Calculate total like: qty × price = item total 💰 and explain simply.

        🛠️ Use tools based on user input:
        - 📜 'get_menu' — show menu.
        - 💾 'save_order' — when user confirms. Format: {{"items": {{"burger": 2}}, "total_price": 12.0}}.
        - ✏️ 'modify_order' — update order. Format: {{"order_id": 101, "items": {{...}}, "total_price": 20.0}}.
        - 🔍 'check_order_status' — order ID (e.g., "101").
        - 📦 'get_order_details' — for full order info.
        - ❌ 'cancel_order' — cancel by order ID.
        - 🙋 'introduce_developer' — introduce yourself (LLM) and your developer in short, friendly text.

        ✅ Be clear, helpful, and kind. End replies with: “Anything else I can help with? 😊”
    """)


    llm = configure_llm(DEFAULT_MODEL_NAME)
    llm_with_tools = llm.bind_tools([get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer])
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages)
    
    logger.info(f"LLM response: {response.content}")
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
    
    return {"messages": [response], "menu": menu}