"""
# DineMate Streaming

This module handles streaming updates for the DineMate foodbot UI using Streamlit.

## Dependencies
- `langchain_core.callbacks`: For streaming callbacks.
- `streamlit`: For UI rendering.
- `graph`: For LangGraph workflow.
- `logger`: For logging.
"""

import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from scripts.graph import build_graph
from scripts.logger import get_logger

logger = get_logger(__name__)

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        """Initialize the StreamHandler."""
        self.container = container
        self.text = initial_text
        logger.info("StreamHandler initialized")

    def on_llm_new_token(self, token: str, **kwargs):
        """Handle new LLM tokens for streaming."""
        self.text += token
        self.container.markdown(self.text)
        logger.debug(f"Received token: {token}")

def stream_graph_updates(user_query: str) -> str:
    """Process a user query using the LangGraph workflow and stream the response."""
    logger.info(f"Processing user query: {user_query}")
    graph = st.session_state.get("graph")
    if not graph:
        graph = build_graph()
        st.session_state["graph"] = graph
        logger.info("Graph initialized and cached")

    config = {'configurable': {'thread_id': '1'}}
    state = graph.invoke({"messages": [{"role": "user", "content": user_query}]}, config=config)
    response = state["messages"][-1].content
    logger.info(f"Response: {response}")
    return response