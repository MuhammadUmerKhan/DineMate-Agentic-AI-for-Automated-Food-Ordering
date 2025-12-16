"""
# DineMate Streaming

This module handles streaming updates for the DineMate foodbot UI using Streamlit.

## Dependencies
- `langchain_core.callbacks`: For streaming callbacks.
- `streamlit`: For UI rendering.
- `graph`: For LangGraph workflow.
- `logger`: For logging.
"""

import streamlit as st, traceback
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
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

async def stream_graph_updates(user_query: str):
    """Streams AI chatbot responses for a user query using LangGraph (Async)."""
    
    logger.info(f"Streaming query: {user_query}")
    graph = st.session_state.get("graph")
    if not graph:
        logger.info("Graph not found, building new graph")
        try:
            graph = build_graph()
            st.session_state["graph"] = graph
            logger.info("Graph initialized")
        except Exception as e:
            logger.error({
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
                "message": "Failed to build graph"
            })
            raise

    config = {'configurable': {'thread_id': 'thread_1'}}
    try:
        async for message_chunk, _ in graph.astream(
            {"messages": [{"role": "user", "content": user_query}]}, 
            config=config, 
            stream_mode="messages"
        ):
            if isinstance(message_chunk, AIMessage):
                yield message_chunk.content
    except Exception as e:
        logger.error({
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "message": "Error during graph streaming"
        })
        raise