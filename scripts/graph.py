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
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from scripts.agent import chatbot, summarize_conversation
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

def build_graph():
    """Construct the LangGraph workflow for the chatbot."""
    logger.info("📈 Building workflow")

    # graph
    builder = StateGraph(State)
    
    # add nodes
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))
    builder.add_node("summarizer", summarize_conversation)

    # add edges
    builder.add_edge(START, "summarizer")
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
