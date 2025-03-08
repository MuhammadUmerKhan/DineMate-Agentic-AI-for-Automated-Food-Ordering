import json
from order.order_handler_lite import OrderHandler
import ast
import re

# ✅ Order Handler for in-memory storage
order_handler = OrderHandler()

# ✅ Define tools
def show_menu(_=None):
    """✅ Return available menu items from stored memory."""
    menu = order_handler.menu  # ✅ Now accessing stored menu
    return f"📜 Here's our menu:\n{menu}" if menu else "⚠ Sorry, the menu is currently unavailable."

def extract_items(order_details):
    """✅ Extracts item names and quantities from structured LLM output and converts them into JSON."""
    try:
        print("🔍 Raw LLM Output:", order_details)  # Debugging

        # ✅ Regular expression to extract items and their quantities
        pattern = r"\(\s*'([^']+)'\s*,\s*(\d+)\s*\)"
        matches = re.findall(pattern, order_details)

        if not matches:
            return "⚠ No valid items found in the input."

        # ✅ Convert extracted data to a structured dictionary
        extracted_order = {item.strip(): int(qty) for item, qty in matches}

        # ✅ Convert to JSON format
        extracted_order_json = json.dumps(extracted_order)

        print("✅ Extracted Order (JSON):", extracted_order_json)  # Debugging

        # ✅ Pass to add_item() for further processing
        response = order_handler.add_item(extracted_order)
        return response

    except Exception as e:
        return f"⚠ Error extracting items: {str(e)}"

def add_items(order_details):
    return extract_items(order_details)
    

def update_item(order_details: str):
    """✅ Extracts item names and quantities using regex from structured order format."""
    try:
        print(f"🔍 Extracting items from: {order_details}")

        # ✅ Use regex to extract item names and quantities
        pattern = r"\(\s*'([\w\s-]+)'\s*,\s*(\d+)\s*\)"  # Matches ('item', quantity)
        matches = re.findall(pattern, order_details)

        if not matches:
            return "⚠ No valid items found. Use structured format like: [('pepsi', 2), ('coca-cola', 3)]"

        # ✅ Convert extracted values into a structured dictionary
        extracted_order = {item.strip().lower(): int(qty) for item, qty in matches}
        print(f"✅ Extracted Order Update: {extracted_order}")

        # ✅ Pass structured dictionary directly to the order handler (Not JSON)
        response = order_handler.update_item(extracted_order)
        return response

    except Exception as e:
        return f"⚠ Error processing update: {str(e)}"

def replace_item(replacements):
    """✅ Replace multiple items in the order while keeping quantity and updating the total price."""
    try:
        print("🔄 Replace Request:", replacements)

        # ✅ Convert string representation of list/tuple to actual Python list
        if isinstance(replacements, str):
            try:
                replacements = ast.literal_eval(replacements)  # Convert string to Python list of tuples
            except (SyntaxError, ValueError):
                return "⚠ Invalid format. Expected [(old_item, new_item), (old_item, new_item), ...]"

        # ✅ Ensure replacements is a list of valid (old_item, new_item) tuples
        if not (isinstance(replacements, list) and all(isinstance(pair, tuple) and len(pair) == 2 for pair in replacements)):
            return "⚠ Invalid format. Expected [(old_item, new_item), (old_item, new_item), ...]"

        # ✅ Process all replacements
        responses = []
        for old_item, new_item in replacements:
            response = order_handler.replace_item(old_item, new_item)
            responses.append(response)

        return "\n".join(responses)  # ✅ Return all updates as a single response

    except Exception as e:
        return f"⚠ Error processing replacement: {str(e)}"


def modify_order_after_confirmation(order_details: str):
    """✅ Modify an order after confirmation before preparation starts."""
    try:
        print(order_details)
        order_data = json.loads(order_details)  # Expecting {'order_id': 1, 'updated_items': {'item': quantity}}
        order_id = order_data["order_id"]
        updated_items = order_data["updated_items"]
        return order_handler.modify_order_after_confirmation(order_id, updated_items)
    except json.JSONDecodeError:
        return "⚠ Invalid format. Use JSON: {'order_id': 1, 'updated_items': {'item': quantity}}"

def confirm_order(_=None):
    """✅ Confirms the order and provides an Order ID."""
    confirmation_message = order_handler.confirm_order()
    return confirmation_message  # ✅ Now returns Order ID after confirmation

def check_order_status(order_id: str):
    """✅ Retrieve order status using Order ID."""
    return order_handler.check_order_status(order_id)

def remove_item(item_name: str):
    """✅ Removes an item from the order."""
    return order_handler.remove_item(item_name)

def total_price(_=None):
    return order_handler.total_price

def check_order_items(_=None):
    return order_handler.order_items

def cancel_order_before_confirmation(_=None):
    """�� Cancels the current order and returns the Order ID."""
    return order_handler.cancel_order_before_confirmation()

def cancel_order_after_confirmation(user_id):
    """🚫 Cancels the current order after confirmation using the Order ID."""
    return order_handler.cancel_order_after_confirmation(user_id)

def estimated_delivery_time(order_id: int):
    """✅ Track estimated delivery time of an order."""
    return order_handler.estimated_delivery_time(order_id)