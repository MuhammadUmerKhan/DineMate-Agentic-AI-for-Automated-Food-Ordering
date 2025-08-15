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
from langsmith import traceable
from scripts.tools import get_full_menu, get_prices_for_items, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer
from scripts.state import State
from scripts.config import LANGCHAIN_PROJECT
from scripts.logger import get_logger
from scripts.utils import configure_llm

logger = get_logger(__name__)

@traceable(run_type="chain", project_name=LANGCHAIN_PROJECT)
def chatbot(state: State) -> State:
    """Process user input and interact with the LLM."""
    messages = state["messages"]
    current_menu = state.get("menu", {})  # Check if menu is already cached

    system_prompt = textwrap.dedent("""
        You are DineMate, a kind, professional AI restaurant assistant 🤖🍽️. 
        Respond clearly, politely, helpfully with emojis (✅=confirm, 📜=menu, 🍔=food, 💰=price). 
        
        For orders (e.g., "2 burgers, 1 coke"):
        - Call get_prices_for_items with the list of mentioned items to validate and get prices.
        - If any item has null price, inform the user it's unavailable.
        - Compute total: qty × unit_price.
        - Confirm details friendly 😊 before saving.
        
        For "show me the menu":
        - If the menu is already available in the session (you'll know from tool results), format it as a concise list (e.g., "Burger: $10, Pizza: $15").
        - Only call get_full_menu if no menu is cached.
        - Do NOT include raw JSON in your response; summarize it nicely.
        
        Tools: 
            - 📜get_full_menu (only if no menu cached and user asks for full menu), 
            - 💰get_prices_for_items (for orders/validation, input: list of item names),
            - 🙋introduce_developer, 
            - 💾save_order (post-confirmation, format: {"items": {"burger": 2}, "total_price": 15.0}), 
            - ✏️modify_order (format: {"order_id": 162, "items": {"pizza": 2}, "total_price": 25.0}), 
            - 🔍check_order_status (with order_id), 
            - 📦get_order_details (with order_id), 
            - ❌cancel_order (with order_id). 
        
        Confirm content/total before saving. End with: “Anything else I can help with?” 😊.
    """)
    
    llm = configure_llm()
    llm_with_tools = llm.bind_tools([get_full_menu, get_prices_for_items, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer])
    messages = [{"role": "system", "content": system_prompt}] + messages
    
    # Pass cached menu to LLM if available, to avoid unnecessary tool calls
    if current_menu:
        messages.append({"role": "assistant", "content": f"Cached menu available: {json.dumps(current_menu, separators=(',', ':'))}"})
    
    response = llm_with_tools.invoke(messages)
    
    logger.info(f"LLM response: {response.content}")
    
    # Handle tool calls and update state
    new_menu = state.get("menu", {})
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
        for tool_call in response.tool_calls:
            if tool_call["name"] == "get_full_menu":
                menu_json = get_full_menu.invoke({})
                try:
                    new_menu = json.loads(menu_json)
                    logger.info("Cached new menu in state")
                except json.JSONDecodeError:
                    logger.error("Invalid menu JSON")
                    new_menu = {}
    
    # Format menu as a user-friendly message if requested
    if response.tool_calls and any(tc["name"] == "get_full_menu" for tc in response.tool_calls):
        if new_menu:
            formatted_menu = "\n".join(f"{item}: ${price:.2f}" for item, price in new_menu.items())
            response.content = f"📜 Here's the menu:\n{formatted_menu}\nAnything else I can help with? 😊"
        else:
            response.content = "⚠️ Menu unavailable.\nAnything else I can help with? 😊"
    
    return {"messages": [response], "menu": new_menu}