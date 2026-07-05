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
from langchain_core.messages import AIMessage
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

async def filter_thinking_stream(async_gen):
    """Filters out any <think>...</think> block from the stream of chunks."""
    buffer = ""
    inside_think = False
    
    async for chunk in async_gen:
        buffer += chunk
        
        while True:
            if not inside_think:
                # Find if START_TAG is in the buffer (case-insensitive)
                idx = buffer.lower().find("<think>")
                if idx != -1:
                    # Yield everything before <think>
                    text_to_yield = buffer[:idx]
                    if text_to_yield:
                        yield text_to_yield
                    # Move past <think>
                    buffer = buffer[idx + 7:]
                    inside_think = True
                else:
                    # Check for partial match of <think> at the end of the buffer
                    partial_match = False
                    for i in range(1, len("<think>")):
                        if buffer.lower().endswith("<think>"[:i]):
                            text_to_yield = buffer[:-i]
                            if text_to_yield:
                                yield text_to_yield
                            buffer = buffer[-i:]
                            partial_match = True
                            break
                    if not partial_match:
                        # No match and no partial match, yield the whole buffer
                        if buffer:
                            yield buffer
                            buffer = ""
                        break
                    else:
                        break
            else:
                # Inside think block, we look for END_TAG
                idx = buffer.lower().find("</think>")
                if idx != -1:
                    # Move past </think>
                    buffer = buffer[idx + 8:]
                    # Strip leading newlines/whitespace that typically follow </think>
                    if buffer.startswith("\n"):
                        buffer = buffer[1:]
                    inside_think = False
                else:
                    # Check for partial match of </think> at the end of the buffer
                    partial_match = False
                    for i in range(1, len("</think>")):
                        if buffer.lower().endswith("</think>"[:i]):
                            buffer = buffer[-i:]
                            partial_match = True
                            break
                    if not partial_match:
                        # Discard the whole buffer since we are inside <think> and no partial match of </think>
                        buffer = ""
                        break
                    else:
                        break
    
    # After generator is done, if we are not inside think, yield any remaining buffer
    if not inside_think and buffer:
        yield buffer

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

    config = {'configurable': {'thread_id': '5'}}

    async def raw_stream():
        async for message_chunk, _ in graph.astream(
            {"messages": [{"role": "user", "content": user_query}]}, 
            config=config, 
            stream_mode="messages"
        ):
            if isinstance(message_chunk, AIMessage):
                yield message_chunk.content

    try:
        async for chunk in filter_thinking_stream(raw_stream()):
            yield chunk
    except Exception as e:
        logger.error({
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "message": "Error during graph streaming"
        })
        raise