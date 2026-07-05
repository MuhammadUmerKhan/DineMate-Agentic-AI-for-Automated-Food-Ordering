import asyncio
import json
from typing import Any, Literal

from langchain_core.messages import HumanMessage

from scripts.config import (
    GUARDRAIL_BLOCK_THRESHOLD,
    GUARDRAIL_BORDERLINE_THRESHOLD,
    GUARDRAIL_MODEL_NAME,
    GUARDRAIL_TIMEOUT_SECONDS,
)
from scripts.logger import get_logger
from scripts.utils import configure_llm

logger = get_logger(__name__)

BLOCKED_RESPONSE = "I can't process that request. How can I help with your order?"

async def guardrail_node(state: dict[str, Any]) -> dict[str, Any]:
    """Classify incoming user messages for prompt-injection risk before the chatbot runs."""
    messages = state.get("messages", []) or []
    if not messages:
        return {"guardrail_status": "PASS", "guardrail_score": 0.0}

    latest_user_message = None
    for message in reversed(messages):
        if isinstance(message, dict):
            if message.get("role") == "user" or message.get("role") == "human":
                latest_user_message = message
                break
        elif getattr(message, "type", None) == "human" or getattr(message, "role", None) == "user":
            latest_user_message = message
            break

    if latest_user_message is None:
        return {"guardrail_status": "PASS", "guardrail_score": 0.0}

    message_content = latest_user_message.get("content", "") if isinstance(latest_user_message, dict) else getattr(latest_user_message, "content", "") or ""
    if not isinstance(message_content, str):
        message_content = json.dumps(message_content)

    if not message_content.strip():
        return {"guardrail_status": "PASS", "guardrail_score": 0.0}

    try:
        llm = configure_llm(GUARDRAIL_MODEL_NAME, streaming=False)
        response = await asyncio.wait_for(
            llm.ainvoke([HumanMessage(content=message_content)], config={"callbacks": []}),
            timeout=GUARDRAIL_TIMEOUT_SECONDS,
        )

        guardrail_score = float(response.content)

        if guardrail_score >= GUARDRAIL_BLOCK_THRESHOLD:
            status = "BLOCK"
            logger.warning("Guardrail BLOCK: score=%.4f message=%r", guardrail_score, message_content)
        elif guardrail_score >= GUARDRAIL_BORDERLINE_THRESHOLD:
            status = "PASS"
            logger.warning("Guardrail BORDERLINE (allowed, flagged): score=%.4f message=%r", guardrail_score, message_content)
        else:
            status = "PASS"
            logger.info("Guardrail PASS: score=%.4f", guardrail_score)

        return {
            "guardrail_status": status,
            "guardrail_score": guardrail_score,
        }
    except asyncio.TimeoutError:
        logger.error("Guardrail evaluation timed out after %.1fs", GUARDRAIL_TIMEOUT_SECONDS)
        return {"guardrail_status": "ERROR", "guardrail_score": None}
    except (ValueError, TypeError) as e:
        logger.error(f"Guardrail returned non-numeric score: {e}")
        return {"guardrail_status": "ERROR", "guardrail_score": None}
    except Exception as e:
        logger.error(f"Guardrail evaluation failed: {e}")
        return {"guardrail_status": "ERROR", "guardrail_score": None}

async def should_continue_after_guardrails(state: dict[str, Any]) -> Literal["PASS", "BLOCK", "ERROR"]:
    """Routing function for the LangGraph conditional edge.
    Returns only the status key; the graph's BLOCK node should return
    BLOCKED_RESPONSE as the user-facing message, and the ERROR node should
    decide whether to fail open or closed.
    """
    status = state.get("guardrail_status", "PASS")

    if status not in ("PASS", "BLOCK", "ERROR"):
        return "ERROR"
    return status