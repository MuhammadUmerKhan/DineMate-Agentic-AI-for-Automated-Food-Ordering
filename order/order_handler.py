import json
import logging
from database.db import Database
import ast
import datetime
# ✅ Configure logging
logging.basicConfig(filename="foodbot.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class OrderHandler:
    def __init__(self):
        """Initialize order handler with menu caching and order storage."""
        self.db = Database()
        self.menu = self.fetch_menu()  # ✅ Store menu once in memory
        self.order_items = {}  # ✅ Stores items in memory until confirmation
        self.total_price = 0.0
        self.user_id = self.db.get_max_id()

    def fetch_menu(self):
        """✅ Fetch and store menu items in memory."""
        try:
            menu = self.db.load_menu()
            if menu:
                return {item["name"].lower(): float(item["price"]) for item in menu}
            else:
                logging.error("⚠ Failed to fetch menu. No items found.")
                return {}
        except Exception as e:
            logging.error(f"⚠ Error fetching menu: {e}")
            return {}

    def add_item(self, items_dict):
        """✅ Adds items to the order while checking availability in menu."""
        response = ""
        for item, quantity in items_dict.items():
            item_lower = item.lower()
            if item_lower in self.menu:
                if item_lower in self.order_items:
                    self.order_items[item_lower] += quantity  # ✅ Update quantity
                else:
                    self.order_items[item_lower] = quantity  # ✅ Add new item
                self.total_price += self.menu[item_lower] * quantity
                response += f"✅ Added {quantity}x {item}.\n"
            else:
                response += f"⚠ {item} is unavailable.\n"

        return response + f"\n🛒 **Updated Order: {self.order_items}**\n💰 **Total Price: ${self.total_price:.2f}**"

    def get_order(self):
        """✅ Returns current order stored in memory."""
        return self.order_items if self.order_items else "No items in order."

    def confirm_order(self):
        """✅ Confirms the order, stores it in the database, and returns the order ID."""
        if not self.order_items:
            return "⚠ No items in your order to confirm."

        total_price = sum(self.menu[item] * quantity for item, quantity in self.order_items.items())

        # ✅ Generate unique order ID
        order_id = self.db.get_max_id()  # ✅ Fetch next available ID

        # ✅ Store the order in the database
        confirmation_message = self.db.store_order(order_id, self.order_items, total_price, "Pending")
        estimated_time = self.db.estimated_delivery_time(order_id)
        # ✅ Reset memory after confirming order
        self.order_items = {}

        return f"✅ Your order has been confirmed! Your Order ID is **{order_id}**.\nUse this ID to check your order status later.\n{confirmation_message} and estimated time to deliver your order is {estimated_time}"

    def remove_item(self, item_name: str):
        """✅ Removes an item from the order and updates total price."""
        if not self.order_items:
            return "⚠ No items in your order to remove."
        
        item_lower = item_name.lower()

        if item_lower in self.order_items:
            removed_quantity = self.order_items[item_lower]
            removed_price = self.menu.get(item_lower, 0) * removed_quantity  # Fetch price from menu

            # Deduct the removed item price from total price
            self.total_price -= removed_price
            del self.order_items[item_lower]

            return (f"✅ Removed **{item_name}** from your order.\n"
                    f"🛒 **Updated Order:** {self.order_items}\n"
                    f"💰 **Updated Total Price: ${self.total_price:.2f}**")
        
        return f"⚠ **{item_name}** is not in your order."



    def update_item(self, order_dict):
        """✅ Updates the quantity of an existing item and adjusts total price."""
        if not isinstance(order_dict, dict):
            return "⚠ Invalid format. Please provide {'item_name': quantity}."

        for item_name, quantity in order_dict.items():
            item_lower = item_name.lower()

            if item_lower in self.order_items:
                old_quantity = self.order_items[item_lower]
                item_price = self.menu.get(item_lower, 0)  # Get price from menu

                # Adjust total price (remove old, add new)
                self.total_price -= old_quantity * item_price
                self.total_price += quantity * item_price

                # Update item quantity
                self.order_items[item_lower] = quantity

                return f"✅ Updated **{item_name}** to **{quantity}**.\n🛒 **Updated Order:** {self.order_items}\n💰 **Total Price: ${self.total_price:.2f}**"
        
        return f"⚠ **{item_name}** is not in your order. Please add it first."

    def estimated_delivery_time(self, order_id):
        """✅ Track estimated delivery time of an order."""
        return self.db.estimated_delivery_time(order_id)
    
    def check_order_status(self, user_id):
        """✅ Retrieve the order status using the stored user ID."""
        return self.db.check_order_status(user_id)

    def cancel_order_before_confirmation(self):
        """✅ Cancels the entire order and resets everything."""
        if not self.order_items:
            return "⚠ You have no active order to cancel."

        self.order_items.clear()
        self.total_price = 0.0

        return "🚫 Your order has been **canceled**. Feel free to start a new order!"

    def cancel_order_after_confirmation(self, user_id):
        """🚫 Cancels the order after confirmation using the stored user ID."""
        return self.db.cancel_order_after_confirmation(user_id)
    
    def replace_item(self, old_item: str, new_item: str):
        """✅ Replace an item in the order while keeping the same quantity and updating price."""
        old_item_lower = old_item.lower()
        new_item_lower = new_item.lower()

        if old_item_lower not in self.order_items:
            return f"⚠ **{old_item}** is not in your order. Please check your order first."

        if new_item_lower not in self.menu:
            return f"⚠ **{new_item}** is not available in the menu."

        # Get old item quantity
        quantity = self.order_items.pop(old_item_lower)

        # Update total price (subtract old price, add new price)
        old_price = self.menu.get(old_item_lower, 0) * quantity
        new_price = self.menu.get(new_item_lower, 0) * quantity
        self.total_price = self.total_price - old_price + new_price

        # Add new item with the same quantity
        self.order_items[new_item_lower] = quantity

        return (f"🔄 Replaced **{old_item}** with **{new_item}**.\n"
                f"🛒 **Updated Order:** {self.order_items}\n"
                f"💰 **Updated Total Price: ${self.total_price:.2f}**")

    def modify_order_after_confirmation(self, order_id, updated_items):
        """✅ Replace an order after confirmation with a new one, ensuring accurate pricing."""
        try:
            # Fetch order details from the database
            sql_query = "SELECT status, time FROM orders WHERE id = %s;"
            self.db.cursor.execute(sql_query, (order_id,))
            result = self.db.cursor.fetchone()

            if not result:
                return f"⚠ No order found with ID {order_id}."

            order_status, order_time = result["status"], result["time"]

            # Ensure time format is correct
            if isinstance(order_time, datetime.timedelta):
                seconds = order_time.total_seconds()
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                order_time = datetime.time(hour=hours, minute=minutes)

            # ✅ Combine with today's date to get full timestamp
            order_time_obj = datetime.datetime.combine(datetime.date.today(), order_time)
            current_time_obj = datetime.datetime.now()

            # Validate time constraints
            time_diff = (current_time_obj - order_time_obj).total_seconds() / 60  
            if time_diff > 20:
                return "⚠ **Your order cannot be modified now. It has been more than 20 minutes.**"
            elif order_status != "Pending":
                return f"⚠ Order {order_id} is already **{order_status}** and cannot be modified."

            # Fetch menu prices
            self.db.cursor.execute("SELECT * FROM menu;")
            menu_items = {item["name"].lower(): float(item["price"]) for item in self.db.cursor.fetchall()}  # ✅ Convert to float

            # Calculate new total price
            new_total_price = 0.0
            final_order = {}

            for item, quantity in updated_items.items():
                item_lower = item.lower()
                if item_lower in menu_items:
                    final_order[item_lower] = quantity
                    new_total_price += menu_items[item_lower] * quantity  # ✅ Ensure float conversion
                else:
                    return f"⚠ **{item} is not available in the menu.** Please select a valid item."

            # Convert updated items to JSON
            updated_items_json = json.dumps(final_order)

            # ✅ Pass updated details to `db.py` to replace the order
            return self.db.modify_order_after_confirmation(order_id, updated_items_json, new_total_price)

        except Exception as e:
            return f"⚠ Error modifying order: {e}"


# Example Usage
# if __name__ == "__main__":
    # handler = OrderHandler()
    # print(handler.fetch_menu())
    # add_items = handler.add_item({"Pepsi": 3})
    # print(add_items)
    # print(handler.get_order())
    # print(handler.confirm_order())
    # print(handler.check_order_status(17))
    # update_order = handler.update_item({"Pepsi": 2})
    # print(update_order)
    
    # replace_item = handler.replace_item("Pepsi", "mango smoothie")
    # print(replace_item)
    
    # modify_order = handler.modify_order_after_confirmation(33, {"fresh orange juice": 3, 'Pepsi': 2})
    # print(modify_order)