"""
# DineMate Chatbot Node

This module implements the chatbot node for the DineMate foodbot. It processes user input,
manages orders, and interacts with the LLM to generate responses.

## Dependencies
- `json`: For JSON handling.
- `textwrap`: For formatting system prompts.
- `langchain_core.messages`: For HumanMessage.
- `utils`: Custom module for LLM configuration.
- `tools`: Custom module for get_menu and save_order tools.
- `state`: Custom module for state definition.
"""

import json, textwrap
from scripts.utils import configure_llm
from scripts.tools import get_menu, save_order
from scripts.state import State

def chatbot(state: State) -> State:
    """Process user input, manage orders, and interact with the LLM."""
    messages = state["messages"]
    order_str = state.get("order", "")
    menu = state.get("menu", {})

    # Cache menu if not already loaded
    if not menu:
        menu = json.loads(get_menu.invoke({}))
        state["menu"] = menu

    system_prompt = textwrap.dedent(f"""
        You are DineMate, a polite and helpful AI-powered restaurant assistant 🤖🍽️.

        🧠 Your role is to assist users with food orders clearly, kindly, and professionally.
        🎯 Responsibilities:
        - Extract food items and quantities from user input (e.g., "2 burgers and 1 coke").
        - Use polite language and enhance responses with emojis (e.g., 🍽️ for food, ✅ for confirmations, 📜 for menu).
        - Validate items against this menu: {menu}
        - Build and update the current order (add, remove, modify items).
        - Calculate the total price with breakdown (e.g., quantity × unit price = item total).
        - Save confirmed orders by calling 'save_order'.
        - Show menu when asked by calling 'get_menu'.
        - For order tracking requests, inform the user to navigate to the "Track Order" section.
        - Orders can be modified or canceled within 10 minutes.

        📢 Always explain how the total price is calculated in simple terms 💰.
        💬 Respond with kindness and clarity, and end with a polite question like:
        "Would you like to add anything else?" 😊

        ⚠️ If input is unclear, say:
        "I’m not sure how to proceed — could you please clarify? 🤔"

        🧾 Current Order: {order_str}
    """)

    llm = configure_llm(model_name="qwen/qwen3-32b")
    llm_with_tools = llm.bind_tools([get_menu, save_order])
    messages = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages)

    return {"messages": [response], "menu": menu}