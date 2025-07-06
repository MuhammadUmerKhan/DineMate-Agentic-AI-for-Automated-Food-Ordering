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
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from scripts.state import State
from scripts.agent import chatbot
from scripts.tools import get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details
from scripts.logger import get_logger

logger = get_logger(__name__)

memory = MemorySaver()

def build_graph():
    """Construct the LangGraph workflow for the chatbot."""
    logger.info("Building LangGraph workflow")
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode([get_menu, save_order, check_order_status, cancel_order, modify_order, get_order_details]))
    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")
    graph = builder.compile(checkpointer=memory)
    logger.info("Graph built successfully")
    return graph

def save_graph_diagram(graph, output_path: str) -> None:
    """Save the LangGraph workflow diagram as a PNG file."""
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(png_data)
        logger.info(f"Diagram saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save diagram: {e}")