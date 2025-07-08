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
from scripts.db import Database
from scripts.logger import get_logger

logger = get_logger(__name__)

@tool
def get_menu() -> str:
    """Fetch the restaurant menu from the database."""
    db = Database()
    try:
        menu = db.load_menu()
        if menu:
            logger.info("Menu fetched successfully")
            return json.dumps(menu)
        logger.warning("No menu items found")
        return "Sorry, the menu is currently unavailable."
    finally:
        db.close_connection()

@tool
def save_order(order_details: str) -> dict:
    """Save the confirmed order to the database.
    :param order_details: JSON string with items and total price, e.g., {'items': {'pizza': 2, 'cola': 1}, 'total_price': 25.0}
    :return: Dictionary with status, message, and order details
    """
    logger.info(f"Received order_details: {order_details}")
    try:
        order_data = json.loads(order_details)
        items = order_data.get("items", {})
        logger.info(f"Items found: {items}")
        total_price = float(order_data.get("total_price", 0.0))

        if not items:
            logger.warning("No items found in order")
            return {
                "status": "empty",
                "message": "No items found in the order.",
                "items": {},
                "total_price": 0.0
            }

        db = Database()
        try:
            order_id = db.store_order_db(items, total_price)
            if order_id:
                logger.info(f"Order saved with ID: {order_id}")
                return {
                    "status": "success",
                    "message": f"Order confirmed with ID {order_id}. Estimated delivery in 40 minutes.",
                    "order_id": order_id,
                    "items": items,
                    "total_price": total_price
                }
            logger.error("Failed to save order to database")
            return {
                "status": "error",
                "message": "Failed to save order.",
                "items": items,
                "total_price": total_price
            }
        finally:
            db.close_connection()
    except json.JSONDecodeError:
        logger.error("Invalid JSON in order_details")
        return {"status": "error", "message": "Failed to parse order. Please provide valid JSON."}

@tool
def check_order_status(order_id: str) -> str:
    """Fetch the order status and estimated delivery time.
    :param order_id: The ID of the order to check (e.g., '162' or 162).
    :return: Status and, if applicable, estimated delivery time or error message.
    """
    logger.info(f"Received order_id: {order_id} (type: {type(order_id)})")
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            logger.error(f"Invalid order_id: {order_id_int}")
            return "Invalid order ID. Please provide a positive integer."
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid order_id format: {order_id}, error: {e}")
        return "Invalid order ID. Please provide a valid number."

    db = Database()
    try:
        result = db.check_order_status_db(order_id_int)
        logger.info(f"Order {order_id_int} status retrieved: {result}")
        return result
    finally:
        db.close_connection()

@tool
def cancel_order(order_id: str) -> str:
    """Cancel an order if within 10 minutes of placement.
    :param order_id: The ID of the order to cancel (e.g., '162' or 162).
    :return: Confirmation or error message.
    """
    logger.info(f"Received order_id: {order_id} (type: {type(order_id)})")
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            logger.error(f"Invalid order_id: {order_id_int}")
            return "Invalid order ID. Please provide a positive integer."
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid order_id format: {order_id}, error: {e}")
        return "Invalid order ID. Please provide a valid number."

    db = Database()
    try:
        result = db.cancel_order_after_confirmation(order_id_int)
        logger.info(f"Order {order_id_int} cancellation result: {result}")
        return result
    finally:
        db.close_connection()

# @tool
def modify_order(order_details: str) -> dict:
    """Modify an existing order within 10 minutes of placement."""
    logger.info(f"Received order_details: {order_details}")
    
    try:
        order_data = json.loads(order_details)
        logger.info(f"JSON loaded: {order_data}")

        order_id = order_data.get("order_id")
        items = order_data.get("items", {})
        total_price = float(order_data.get("total_price", 0.0))

        if not order_id or not isinstance(order_id, (str, int)) or int(order_id) <= 0:
            logger.error(f"Invalid order_id: {order_id}")
            return {"status": "error", "message": "Invalid order ID. Please provide a positive number."}
        
        if not items:
            logger.warning("No items found in order")
            return {"status": "empty", "message": "No items found in the updated order.", "items": {}, "total_price": 0.0}

        order_id = int(order_id)
        logger.info(f"Extracted ➤ Order ID: {order_id}, Items: {items}, Price: {total_price}")

        db = Database()
        try:
            result = db.modify_order_after_confirmation(order_id, json.dumps(items), total_price)
            logger.info(f"Order {order_id} modification result: {result}")
            
            return {
                "status": "success" if "successfully updated" in result else "error",
                "message": result,
                "order_id": order_id,
                "items": items,
                "total_price": total_price
            }
        finally:
            db.close_connection()

    except json.JSONDecodeError:
        logger.error("Invalid JSON in order_details")
        return {"status": "error", "message": "Failed to parse order details. Please provide valid JSON."}

    except ValueError as e:
        logger.error(f"Invalid total_price format: {e}")
        return {"status": "error", "message": "Invalid total price. Please provide a valid number."}

@tool
def get_order_details(order_id: str) -> dict:
    """Retrieve order details and modification eligibility.
    :param order_id: JSON string with order_id, e.g., {"order_id": 162}
    :return: Dictionary with order details, status, and eligibility message.
    """
    logger.info(f"Received order_id: {order_id} (type: {type(order_id)}")
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            logger.error(f"Invalid order_id: {order_id_int}")
            return "Invalid order ID. Please provide a positive integer."
        db = Database()
        try:
            result = db.get_order_by_id(order_id_int)
            logger.info(f"Order {order_id_int} details retrieved: {result['message']}")
            return result
        finally:
            db.close_connection()
    except json.JSONDecodeError:
        logger.error("Invalid JSON in order_details")
        return {"status": "error", "message": "Failed to parse order details. Please provide valid JSON."}

@tool
def introduce_developer() -> str:
    """
    Introduce the LLM assistant and the creator of the DineMate project.
    """
    return (
        "👋 Hello! I’m your friendly AI assistant powered by an advanced LLM, here to help you order food 🍔, "
        "track orders 🚚, and manage your experience with ease and a smile. 😊\n\n"
        "This tool is developed by Muhammad Umer Khan — an AI Engineer focused on building smart, agentic systems using LLMs, NLP, and MLOps. "
        "He builts **DineMate**, an AI-powered food ordering assistant that simplifies menu browsing, order placing, and status tracking, "
        "built with LangGraph, LLM tools, and Streamlit.\n\n"
        "🔗 Connect with me:\n"
        "• LinkedIn: https://www.linkedin.com/in/muhammad-umer-khan-61729b260/\n"
        "• GitHub: https://github.com/MuhammadUmerKhan\n\n"
        "Need anything else? I'm here to assist! 🤖🍽️"
    )
