"""
# DineMate Graph Builder

This module constructs the LangGraph workflow for the DineMate foodbot.

## Dependencies
- `os`: For file path handling.
- `langgraph.graph`: For StateGraph and START.
- `langgraph.prebuilt`: For ToolNode and tools_condition.
- `langgraph.checkpoint.memory`: For MemorySaver.
- `state`: For state definition.
- `agent`: For chatbot node.
- `tools`: For get_menu and save_order tools.
- `logger`: For logging.
"""

import os
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from scripts.agent import chatbot, summarize_conversation
from scripts.guardrails import guardrail_node, should_continue_after_guardrails, BLOCKED_RESPONSE
from scripts.logger import get_logger
from scripts.state import State
from scripts.tools import (
    get_full_menu, get_prices_for_items, save_order, 
    check_order_status, cancel_order, modify_order, 
    get_order_details, introduce_developer
    )

logger = get_logger(__name__)
memory = MemorySaver()

tools = [
    get_full_menu, get_prices_for_items, save_order, 
    check_order_status, cancel_order, modify_order, 
    get_order_details, introduce_developer
]

def blocked_response_node(state: State) -> dict:
    """Terminal node reached when the guardrail blocks a message.
    Surfaces a generic refusal instead of silently dropping the turn."""
    logger.warning("Guardrail BLOCK path reached — returning refusal to user")
    return {"messages": [AIMessage(content=BLOCKED_RESPONSE)]}


def build_graph():
    """Construct the LangGraph workflow for the chatbot."""
    logger.info("📈 Building workflow")

    # graph
    builder = StateGraph(State)
    
    # add nodes
    builder.add_node("guardrails", guardrail_node)
    builder.add_node("blocked", blocked_response_node)
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))
    builder.add_node("summarizer", summarize_conversation)

    # add edges
    # Guardrail runs first, before the costlier summarizer/chatbot calls,
    # so a blocked message never reaches the LLM agent or its tools.
    builder.add_edge(START, "guardrails")
    builder.add_conditional_edges(
        "guardrails",
        should_continue_after_guardrails,
        {
            "PASS": "summarizer",
            "BLOCK": "blocked",
            # Fail-open on classifier error: this is a defense-in-depth layer,
            # not the only control (see tools.py/db.py fixes), so an
            # unavailable guardrail shouldn't take down ordering entirely.
            "ERROR": "summarizer",
        },
    )
    builder.add_edge("blocked", END)
    builder.add_edge("summarizer", "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")

    try:
        graph = builder.compile(checkpointer=memory)
        logger.info("✅ Graph built successfully")
        return graph
    except Exception as e:
        logger.error(f"❌ Failed to build graph: {str(e)}")
        raise

def save_graph_diagram(graph, output_path: str) -> None:
    """Save the LangGraph workflow diagram as a PNG file."""
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(png_data)
        logger.info("🖼️ Diagram saved")
    except Exception as e:
        logger.error({"error": str(e), "message": "❌ Diagram save failed"})
