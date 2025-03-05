import json
from order.order_handler import OrderHandler
import ast

# ✅ Order Handler for in-memory storage
order_handler = OrderHandler()

# ✅ Define tools
def show_menu(_=None):
    """✅ Return available menu items from stored memory."""
    menu = order_handler.menu  # ✅ Now accessing stored menu
    return f"📜 Here's our menu:\n{menu}" if menu else "⚠ Sorry, the menu is currently unavailable."

def take_order(order_details: str):
    """✅ Extracts and stores order items in memory."""
    # print(order_details)  # ✅ Debugging: Print raw LLM output

    try:
        order_dict = json.loads(order_details)
        print(order_dict)  # ✅ Debugging: Print parsed JSON
        if not isinstance(order_dict, dict):
            return "⚠ Invalid format. Use JSON format: {'item': quantity}"

        response = order_handler.add_item(order_dict)  # ✅ Add to memory
        return response
    except json.JSONDecodeError:
        return "⚠ Invalid JSON format. Please use structured order format."

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

def update_item(item_details: str):
    """Update the quantity of an existing item in the order."""
    try:
        order_dict = json.loads(item_details)  # Expecting {"item": new_quantity}
        print(order_dict)
        if not isinstance(order_dict, dict):
            return "Invalid format. Use JSON format: {'item': quantity}"
        
        response = order_handler.update_item(order_dict)
        return response
    except json.JSONDecodeError:
        return "Invalid JSON format. Use structured order format."

def cancel_order_before_confirmation(_=None):
    """�� Cancels the current order and returns the Order ID."""
    return order_handler.cancel_order_before_confirmation()

def cancel_order_after_confirmation(user_id):
    """🚫 Cancels the current order after confirmation using the Order ID."""
    return order_handler.cancel_order_after_confirmation(user_id)


def replace_item(replacements):
    """✅ Replace multiple items in the order while keeping the same quantity and updating the total price."""
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

def estimated_delivery_time(order_id: int):
    """✅ Track estimated delivery time of an order."""
    return order_handler.estimated_delivery_time(order_id)

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
