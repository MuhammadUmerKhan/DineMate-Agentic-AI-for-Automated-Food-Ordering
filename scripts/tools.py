"""
# DineMate Tools

This module defines the tools for the DineMate foodbot, including fetching the menu and
saving orders to the database. Tools are implemented using LangChain's tool decorator.

## Dependencies
- `json`: For JSON handling.
- `langchain_core.tools`: For tool decorator.
- `langchain_core.messages`: For HumanMessage.
- `utils`: Custom module for LLM configuration.
- `SQLLITE_db`: Custom module for database operations.
"""

import json
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from scripts.utils import configure_llm
from scripts.db import Database

@tool
def get_menu() -> str:
    """Fetch the restaurant menu from the database."""
    db = Database()
    try:
        menu = db.load_menu()
        return json.dumps(menu) if menu else "⚠️ Sorry, the menu is currently unavailable."
    finally:
        db.close_connection()

@tool
def save_order(order_details: str) -> dict:
    """Extract items and price using LLM and save the order to the database."""
    order_details = order_details.strip()
    llm = configure_llm(model_name="meta-llama/llama-4-scout-17b-16e-instruct")

    try:
        response = llm.invoke([
            HumanMessage(content=f"""
                You are a helpful food-ordering assistant 🍽️
                Task:
                - Extract items and price from the text.
                - Return only valid JSON: {{"items": {{"burger": 2}}, "total_price": 300.0}}
                - If nothing is ordered, return: {{"items": {{}}, "total_price": 0.0}}
                Text:
                {order_details}
            """)
        ])

        # Extract JSON from response
        content = response.content.strip()
        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        extracted_json = content[json_start:json_end]
        order_data = json.loads(extracted_json)

        items = order_data.get("items", {})
        total_price = order_data.get("total_price", 0.0)

        if not items:
            return {
                "status": "empty",
                "message": "⚠️ No items found in the order.",
                "items": {},
                "total_price": 0.0
            }

        db = Database()
        try:
            order_id = db.store_order(items, total_price)
            if order_id:
                return {
                    "status": "success",
                    "message": f"✅ Order confirmed with ID {order_id}. Estimated delivery in 40 minutes.",
                    "order_id": order_id,
                    "items": items,
                    "total_price": total_price
                }
            else:
                return {
                    "status": "error",
                    "message": "⚠️ Failed to save order.",
                    "items": items,
                    "total_price": total_price
                }
        finally:
            db.close_connection()

    except json.JSONDecodeError:
        return {"status": "error", "message": "⚠️ Failed to parse order. Please try again."}
    except Exception as e:
        return {"status": "error", "message": f"⚠️ An error occurred: {str(e)}"}