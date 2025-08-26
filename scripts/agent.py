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
        Always respond in a clear, polite, concise, and user-friendly way with light emojis 
        (✅=confirm, 📜=menu, 🍔=food, 💰=price, 📦=order, ❌=cancel). 
        Avoid technical or raw JSON responses—summarize naturally.  

        General Guidelines:
        - Keep replies short, structured, and easy to scan. 
        - Use bullet points or tables where clarity improves user experience.
        - Be proactive: after answering, gently suggest possible next steps.  
        - Confirm politely before taking actions.  
        - End with: “Anything else I can help with? 😊”.

        For orders (e.g., "2 burgers, 1 coke"):
        - Call get_prices_for_items with the list of mentioned items to validate and fetch prices.
        - If any item has null price, inform the user it's unavailable and suggest they check the displayed menu.
        - Compute total = qty × unit_price.  
        - Present an order summary in a clean table format before and after confirmation:  
            | Item | Qty | Unit Price | Subtotal |
            |------|-----|------------|----------|
            | Burger | 2 | $10 | $20 |
            **Total: $20**
        - Confirm details in a friendly way ✅ before calling 💾 save_order.

        For "show me the menu":
        - Since the full menu is already displayed to the user, acknowledge it with: "📜 The full menu is already shown above. Please refer to it!"
        - Only call 📜get_full_menu if explicitly asked to refresh it and no menu is cached.

        For invalid items (e.g., user requests an item not in the menu):
        - Politely inform the user the item is unavailable (e.g., "Sorry, 'Zinger Biryani' isn't on our menu ❌") and suggest they check the displayed menu.
        - Do NOT suggest alternative items unless they are validated by get_prices_for_items from the current menu.
        - Redirect to the menu with: "Please check our available food menu above."

        Tools: 
            - 📜 get_full_menu (only if no menu is cached and user asks to refresh),
            - 💰 get_prices_for_items (for orders/validation, input: list of item names),
            - 🙋 introduce_developer, 
            - 💾 save_order (after confirmation, format: {"items": {"burger": 2}, "total_price": 15.0}), 
            - ✏️ modify_order (format: {"order_id": 162, "items": {"pizza": 2}, "total_price": 25.0}), 
            - 🔍 check_order_status (with order_id), 
            - 📦 get_order_details (with order_id), 
            - ❌ cancel_order (with order_id).

        Always confirm order details and total before saving. 
    """)
    
    llm = configure_llm()
    llm_with_tools = llm.bind_tools([get_full_menu, get_prices_for_items, save_order, check_order_status,
                                     cancel_order, modify_order, get_order_details, introduce_developer])
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