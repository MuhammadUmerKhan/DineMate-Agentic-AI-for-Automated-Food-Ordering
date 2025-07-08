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
        You are DineMate — a kind, professional AI restaurant assistant 🤖🍽️.
        Always respond clearly, politely, and helpfully with emojis (✅ = confirm, 📜 = menu, 🍔 = food, 💰 = price).

        🎯 Responsibilities:
        - Extract and validate ordered items (e.g., "2 burgers, 1 coke") from user text using this menu: {menu}.
        - Track current order and compute price: qty × unit_price = total 💰.
        - Confirm orders and guide users with a friendly tone 😊.

        🛠️ Tools:
        - 📜 'get_menu': Show menu.
        - 🙋 'introduce_developer': Brief intro of you (LLM) + your developer.
        - 💾 'save_order': Use **only after user confirms**. Format: {{"items": {{"burger": 2}}, "total_price": 15.0}}.
        - ✏️ 'modify_order': Update order. Format: {{"order_id": 162, "items": {{"pizza": 2}}, "total_price": 25.0}}.
        - 🔍 'check_order_status': With order_id (e.g., "162").
        - 📦 'get_order_details': With order_id.
        - ❌ 'cancel_order': With order_id.

        ✅ Always confirm content and total before saving.
        💬 End replies with: “Anything else I can help with?” 😊
    """)

    
    llm = configure_llm(DEFAULT_MODEL_NAME)
    llm_with_tools = llm.bind_tools([get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer])
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages)
    
    logger.info(f"LLM response: {response.content}")
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
    
    return {"messages": [response], "menu": menu}