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
from scripts.tools import get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer
from scripts.state import State
from scripts.config import LANGCHAIN_PROJECT
from scripts.logger import get_logger
from scripts.utils import configure_llm

logger = get_logger(__name__)

@traceable(run_type="chain", project_name=LANGCHAIN_PROJECT)
def chatbot(state: State) -> State:
    """Process user input and interact with the LLM."""
    messages = state["messages"]

    system_prompt = textwrap.dedent("""
        You are DineMate, a kind, professional AI restaurant assistant 🤖🍽️. 
        Respond clearly, politely, helpfully with emojis (✅=confirm, 📜=menu, 🍔=food, 💰=price). 
        Use the get_menu tool to fetch the menu when needed to validate items or compute prices (e.g., "2 burgers, 1 coke"). 
        Track order, compute price (qty × unit_price = total 💰). Confirm orders friendly 😊. 
        
        Tools: 
            - 📜get_menu (call to fetch menu), 
            - 🙋introduce_developer, 
            - 💾save_order (post-confirmation, format: {"items": {"burger": 2}, "total_price": 15.0}), 
            - ✏️modify_order (format: {"order_id": 162, "items": {"pizza": 2}, "total_price": 25.0}), 
            - 🔍check_order_status (with order_id), 
            - 📦get_order_details (with order_id), 
            - ❌cancel_order (with order_id). 
            
        Confirm content/total before saving. End with: “Anything else I can help with?” 😊.
    """)
    
    llm = configure_llm()
    llm_with_tools = llm.bind_tools([get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details, introduce_developer])
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages)
    
    logger.info(f"LLM response: {response.content}")
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
        for tool_call in response.tool_calls:
            if tool_call["name"] == "get_menu":
                menu = json.loads(get_menu.invoke({}))
                state["menu"] = menu
                logger.info("Cached menu in state after get_menu call")
    
    return {"messages": [response], "menu": state.get("menu", {})}