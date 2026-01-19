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
from scripts.state import State
from scripts.logger import get_logger
from scripts.utils import configure_llm
from scripts.config import MODEL_NAME, DEFAULT_MODEL_NAME
from scripts.prompt import FOODBOT_PROMPT, SUMMARIZE_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from scripts.config import LANGSMITH_PROJECT, SUMMARY_MESSAGE_THRESHOLD, KEEP_LAST_MESSAGES
from scripts.tools import (get_full_menu, get_prices_for_items, save_order, check_order_status, 
                    cancel_order, modify_order, get_order_details, introduce_developer)

logger = get_logger(__name__)

# =================================== Summarize conversation  ======================================
@traceable(run_type="chain", name="DineMate_ChatFlow", project_name=LANGSMITH_PROJECT)
async def summarize_conversation(state: State):
    """Summarize the conversation history to save tokens."""
    existing_summary = state.get("summary", "")

    # We summarize everything except the very last few messages
    # (we'll keep last 4–6 verbatim anyway)
    if len(state["messages"]) < SUMMARY_MESSAGE_THRESHOLD:
        return state  # too short → no need

    # Take all messages except the last 4
    messages_to_summarize = state["messages"][:-KEEP_LAST_MESSAGES]

    # Build content string from messages
    content = "\n".join(
        f"{msg.type.upper()}: {msg.content}"
        for msg in messages_to_summarize
        if hasattr(msg, "content") and msg.content.strip()
    )

    # Fill the prompt with existing_summary and new content
    filled_system_content = SUMMARIZE_PROMPT.format(
        existing_summary=existing_summary if existing_summary else "None",
        conversation=content
    )

    prompt = [
        SystemMessage(content=filled_system_content),
        HumanMessage(content="Produce the updated bullet-point summary now.")
    ]

    try:
        llm = configure_llm(MODEL_NAME, force_reload=True)
        summary_msg = await llm.ainvoke(prompt)
        new_summary = summary_msg.content.strip()

        # Decide which old messages to remove. Keep last 4 messages + remove older ones
        messages_to_remove = [
            RemoveMessage(id=msg.id)
            for msg in state["messages"][:-KEEP_LAST_MESSAGES]
        ]

        logger.info(f"✅ Conversation summarized. New summary length: {len(new_summary)} chars")

        return {
            "summary": new_summary,
            "messages": messages_to_remove,
        }

    except Exception as e:
        logger.error(f"❌ Summarization failed: {e}")
        return {}   # fail silently — better than crashing
# ==================================================================================================


# ===================================  Dinemate Agent  ==================================================
@traceable(run_type="chain", name="DineMate_ChatFlow", project_name=LANGSMITH_PROJECT)
async def chatbot(state: State) -> State:
    """Process user input and interact with the LLM (Async)."""
    messages = state["messages"]
    current_menu = state.get("menu", {})  # Check if menu is already cached
    
    system_prompt = textwrap.dedent(FOODBOT_PROMPT)

    if state.get("summary"):
        system_prompt += f"\n\n=== Conversation summary so far ===\n{state['summary']}\n"
    
    llm = configure_llm(DEFAULT_MODEL_NAME)
    llm_with_tools = llm.bind_tools(
        [get_full_menu, get_prices_for_items, save_order, check_order_status,
        cancel_order, modify_order, get_order_details, introduce_developer]
    )
    
    messages = [SystemMessage(content=system_prompt)] + messages
    
    # Pass cached menu to LLM if available, to avoid unnecessary tool calls
    if current_menu:
        messages.append({
            "role": "assistant", 
            "content": f"Cached menu available: {json.dumps(current_menu, separators=(',', ':'))}"
            })
    
    response = await llm_with_tools.ainvoke(messages)
    
    logger.info(f"💬 LLM response: {response.content}")
    
    # Handle tool calls and update state
    new_menu = state.get("menu", {})
    if response.tool_calls:
        logger.info(f"Tool calls: {response.tool_calls}")
        for tool_call in response.tool_calls:
            if tool_call["name"] == "get_full_menu":
                menu_json = await get_full_menu.ainvoke({})
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
# ==================================================================================================