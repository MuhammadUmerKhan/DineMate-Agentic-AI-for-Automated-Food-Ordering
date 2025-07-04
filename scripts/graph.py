"""
# DineMate Graph Builder

This module constructs the LangGraph workflow for the DineMate foodbot and provides a function
to save the workflow diagram as a PNG file.

## Dependencies
- `os`: For file path handling.
- `langgraph.graph`: For StateGraph and START.
- `langgraph.prebuilt`: For ToolNode and tools_condition.
- `langgraph.checkpoint.memory`: For MemorySaver.
- `state`: Custom module for state definition.
- `chatbot`: Custom module for chatbot node.
- `tools`: Custom module for get_menu and save_order tools.
"""

import os
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from scripts.state import State
from scripts.agent import chatbot
from scripts.tools import get_menu, save_order

# Initialize memory for state persistence
memory = MemorySaver()

def build_graph():
    """Construct the LangGraph workflow for the chatbot."""
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode([get_menu, save_order]))
    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")
    return builder.compile(checkpointer=memory)

def save_graph_diagram(graph, output_path: str) -> None:
    """
    Save the LangGraph workflow diagram as a PNG file to the specified path.

    Args:
        graph: The compiled LangGraph object.
        output_path (str): The file path where the PNG diagram will be saved.
    """
    try:
        # Generate PNG data
        png_data = graph.get_graph().draw_mermaid_png()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save PNG data to file
        with open(output_path, "wb") as f:
            f.write(png_data)
        print(f"✅ Diagram saved successfully to {output_path}")
    except Exception as e:
        print(f"⚠️ Failed to save diagram: {str(e)}")