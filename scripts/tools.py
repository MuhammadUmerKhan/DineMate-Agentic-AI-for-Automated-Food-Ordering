"""
# DineMate Tools

This module defines tools for the DineMate foodbot, including fetching the menu and
saving orders to the database.

## Dependencies
- `json`: For JSON handling.
- `langchain_core.tools`: For tool decorator.
- `db`: Custom module for database operations.
- `logger`: Custom module for logging.
"""

import json
from langchain_core.tools import tool
from scripts.db import AsyncDatabase
from scripts.logger import get_logger
from scripts.order_utils import coerce_order_payload, fetch_price_lookup, recompute_total_price

logger = get_logger(__name__)

@tool
async def get_full_menu() -> dict:
    """Fetch the full restaurant menu as a compact JSON string. Use ONLY when the user explicitly asks to see the entire menu."""
    async with AsyncDatabase() as db:
        menu = await db.load_menu()
        if menu:
            logger.info("🍔 Full menu fetched")
            return json.dumps(menu, separators=(",", ":"))
        logger.warning("⚠️ No menu items found")
        return "Menu unavailable."

@tool
async def get_prices_for_items(items: list) -> str:
    """Fetch prices for a specific list of items as a compact JSON dict (e.g., {'burger': 10.0, 'coke': 2.0}). 
    Returns null for any invalid items. Use this for validating items and calculating prices during orders.
    
    :param items: List of item names (e.g., ['burger', 'coke']).
    """
    prices = await fetch_price_lookup(items)
    logger.info(f"💰 Prices fetched for {len(items)} items")
    return json.dumps(prices, separators=(",", ":"))

@tool
async def save_order(order_details: dict | str) -> dict:
    """Save the confirmed order to the database.
    :param order_details: Either a JSON string or a structured object with items and total price, e.g., {'items': {'pizza': 2, 'cola': 1}, 'total_price': 25.0}
    :return: Dictionary with status, message, and order details
    """
    logger.info("💾 Received order")
    order_data, payload_error = coerce_order_payload(order_details)
    if payload_error:
        logger.error(f"❌ {payload_error}")
        return {"status": "error", "message": payload_error}

    try:
        items = order_data.get("items", {})
        logger.info("🍽️ Items found")

        if not items:
            logger.warning("⚠️ No items in order")
            return {"status": "empty", "message": "No items.", "items": {}, "total_price": 0.0}

        total_price, price_error = await recompute_total_price(items)
        if price_error:
            logger.error(f"❌ {price_error}")
            return {"status": "error", "message": price_error, "items": items, "total_price": 0.0}

        async with AsyncDatabase() as db:
            order_id = await db.store_order_db(items, total_price)
            if order_id:
                logger.info("✅ Order saved")
                return {"status": "success", "message": f"Order {order_id} confirmed. Delivery in 40 min.", "order_id": order_id, "items": items, "total_price": total_price}
            logger.error("❌ Failed to save order")
            return {"status": "error", "message": "Save failed.", "items": items, "total_price": total_price}
    except Exception as exc:
        logger.error(f"❌ Failed to save order: {exc}")
        return {"status": "error", "message": "Failed to save order."}

@tool
async def check_order_status(order_id: str) -> str:
    """Fetch the order status and estimated delivery time.
    :param order_id: The ID of the order to check (e.g., '162' or 162).
    :return: Status and, if applicable, estimated delivery time or error message.
    """
    logger.info("📦 Checking status")
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            logger.error("❌ Invalid order ID")
            return "Invalid ID."
    except (ValueError, TypeError) as e:
        logger.error("❌ Invalid ID format")
        return "Invalid number."

    async with AsyncDatabase() as db:
        result = await db.check_order_status_db(order_id_int)
        logger.info("✅ Status retrieved")
        return result

@tool
async def cancel_order(order_id: str) -> str:
    """Cancel an order if within 10 minutes of placement.
    :param order_id: The ID of the order to cancel (e.g., '162' or 162).
    :return: Confirmation or error message.
    """
    logger.info("🚫 Canceling order")
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            logger.error("❌ Invalid order ID")
            return "Invalid ID."
    except (ValueError, TypeError) as e:
        logger.error("❌ Invalid ID format")
        return "Invalid number."

    async with AsyncDatabase() as db:
        result = await db.cancel_order_after_confirmation(order_id_int)
        logger.info("✅ Cancellation result")
        return result

@tool
async def modify_order(order_details: dict | str) -> dict:
    """Modify an existing order using the latest menu-based prices.

    Args:
        order_details: Either a JSON string or a dictionary containing the order ID,
            updated items, and the caller-provided total price.

    Returns:
        A dictionary describing the modification result, including the recomputed total.
    """
    logger.info("✍️ Modifying order")
    order_data, payload_error = coerce_order_payload(order_details)
    if payload_error:
        logger.error(f"❌ {payload_error}")
        return {"status": "error", "message": payload_error}

    try:
        logger.info("✅ JSON loaded")

        order_id = order_data.get("order_id")
        items = order_data.get("items", {})

        if not order_id or not isinstance(order_id, (str, int)) or int(order_id) <= 0:
            logger.error("❌ Invalid order ID")
            return {"status": "error", "message": "Invalid ID."}
        
        if not items:
            logger.warning("⚠️ No items in update")
            return {"status": "empty", "message": "No items.", "items": {}, "total_price": 0.0}

        total_price, price_error = await recompute_total_price(items)
        if price_error:
            logger.error(f"❌ {price_error}")
            return {"status": "error", "message": price_error, "items": items, "total_price": 0.0}

        order_id = int(order_id)
        logger.info("🔧 Order data extracted")

        async with AsyncDatabase() as db:
            result = await db.modify_order_after_confirmation(order_id, json.dumps(items), total_price)
            logger.info("✅ Modification result")
            return {
                "status": "success" if "successfully updated" in result else "error",
                "message": result,
                "order_id": order_id,
                "items": items,
                "total_price": total_price
            }

    except ValueError as e:
        logger.error("❌ Invalid price")
        return {"status": "error", "message": "Invalid price."}
    except Exception as exc:
        logger.error(f"❌ Failed to modify order: {exc}")
        return {"status": "error", "message": "Failed to modify order."}

@tool
async def get_order_details(order_id: str) -> dict:
    """Retrieve order details and modification eligibility.
    :param order_id: JSON string with order_id, e.g., {"order_id": 162}
    :return: Dictionary with order details, status, and eligibility message.
    """
    logger.info("🔍 Fetching order details")
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            logger.error("❌ Invalid order ID")
            return "Invalid ID."
        async with AsyncDatabase() as db:
            result = await db.get_order_by_id(order_id_int)
            logger.info("✅ Details retrieved")
            return result
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON")
        return {"status": "error", "message": "Invalid JSON."}

@tool
def introduce_developer() -> str:
    """
    Introduce the LLM assistant and the creator of the DineMate project.
    """
    return (
        """👋 I'm DineMate, powered by LLM, created by Muhammad Umer Khan, AI Engineer.
        - LinkedIn: https://www.linkedin.com/in/muhammad-umer-khan-61729b260/, 
        - GitHub: https://github.com/MuhammadUmerKhan?tab=repositories. 
        Anything else? 😊"""
    )
