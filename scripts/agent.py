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
from scripts.tools import get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details
from scripts.state import State
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
        You are DineMate 🤖🍽️ — a polite, friendly AI assistant for restaurant ordering.

        🎯 Tasks:
        - Understand user input like "2 zingers, 1 fries", and validate items from menu: {menu}.
        - Keep the current order updated in memory.
        - Calculate and show total as: qty × price = item total 💰.
        - Explain total briefly in a clear, simple way.

        🛠️ Tool usage:
        - 📜 'get_menu' — show the full menu.
        - 💾 'save_order' — only when user says "confirm". Format: {{"items": {{"burger": 2}}, "total_price": 12.0}}.
        - ✏️ 'modify_order' — update order. Format: {{"order_id": 101, "items": {{...}}, "total_price": 20.0}}.
        - 🔍 'check_order_status' — takes order ID (e.g., "101").
        - 📦 'get_order_details' — for order info using ID.
        - ❌ 'cancel_order' — cancel with order ID.

        ✅ Be clear and helpful. End replies with: “Anything else I can help with? 😊”
    """)

    llm = configure_llm(model_name="qwen/qwen3-32b")
    llm_with_tools = llm.bind_tools([get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details])
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages)
    
    logger.info(f"LLM response: {response.content}")
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
    
    return {"messages": [response], "menu": menu}