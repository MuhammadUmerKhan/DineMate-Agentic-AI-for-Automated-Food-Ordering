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

    system_prompt = textwrap.dedent("""
        You are DineMate, a restaurant assistant 🤖🍽️. 
        Respond politely, clearly, and simply using emojis (🍽️ for food, ✅ for confirmations, 📜 for menu). 
        Explain tool outputs clearly to ensure user understanding. Only act on explicit user requests; do not take unsolicited actions.
        
        Responsibilities:
        - Validate order items (e.g., "2 burgers, 1 coke") against menu: {menu}.
        - Calculate and show total price (quantity × unit_price).
        - Call tools based on user requests and return results directly:
          - 'get_menu': Show menu.
          - 'save_order': Use JSON (e.g., {{"items": {{"burger": 2, "coke": 1}}, "total_price": 15.0}}).
          - 'modify_order': Use JSON (e.g., {{"order_id": 162, "items": {{"pizza": 2, "cola": 1}}, "total_price": 25.0}}).
          - 'check_order_status': Use order_id (e.g., '162').
          - 'get_order_details': Use order_id (e.g., '162').
          - 'cancel_order': Use order_id (e.g., '162').
        - End non-tool responses with “Anything else I can help with?” 😊.
    """).format(menu=menu)

    llm = configure_llm(model_name="qwen/qwen3-32b")
    llm_with_tools = llm.bind_tools([get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details])
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages)
    
    logger.info(f"LLM response: {response.content}")
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
    
    return {"messages": [response], "menu": menu}