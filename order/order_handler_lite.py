import json
import logging
import datetime
from database.SQLLITE_db import Database  # ✅ SQLite Database Connection

# ✅ Configure logging
logging.basicConfig(filename="foodbot.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class OrderHandler:
    def __init__(self):
        """✅ Initialize order handler with menu caching and order storage."""
        self.db = Database()
        self.menu = self.fetch_menu()  # ✅ Cache menu in memory
        self.order_items = {}  # ✅ Stores items in memory until confirmation
        self.total_price = 0.0

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
        """✅ Adds items to the order while checking availability in the menu and suggesting available items."""
        response = ""
        unavailable_items = []  # List to store unavailable items

        for item, quantity in items_dict.items():
            item_lower = item.lower()
            if item_lower in self.menu:
                self.order_items[item_lower] = self.order_items.get(item_lower, 0) + quantity
                self.total_price += self.menu[item_lower] * quantity
                response += f"✅ Added {quantity}x {item}.\n"
            else:
                unavailable_items.append(item)  # Store unavailable item

        # ✅ If there are unavailable items, suggest available ones
        if unavailable_items:
            available_items_list = ", ".join([f"**{item.title()}**" for item in self.menu.keys()])
            response += f"\n⚠ The following items are unavailable: {', '.join(unavailable_items)}.\n"
            response += f"📌 Available items: {available_items_list}.\n"

        return response + f"\n🛒 **Updated Order: {self.order_items}**\n💰 **Total Price: ${self.total_price:.2f}**"


    def get_order(self):
        """✅ Returns the current order stored in memory."""
        return self.order_items if self.order_items else "⚠ No items in order."

    def confirm_order(self):
        """✅ Confirms and stores the order in the database."""
        if not self.order_items:
            return "⚠ No items in your order to confirm."

        total_price = sum(self.menu[item] * quantity for item, quantity in self.order_items.items())

        order_id = self.db.get_max_id()  # ✅ Fetch next available ID
        
        # ✅ Store the order in SQLite
        confirmation_message = self.db.store_order(self.order_items, total_price, "Pending")
        estimated_time = self.db.estimated_delivery_time(order_id)
        
        # ✅ Reset memory after confirming the order
        self.order_items = {}

        return f"✅ Your order has been confirmed!\n{confirmation_message}\n and this is your ID {order_id} remember this to track your order \n ⏳ Estimated Delivery Time: {estimated_time}"

    def remove_item(self, item_name):
        """✅ Removes an item from the order and updates the total price."""
        item_lower = item_name.lower()

        if item_lower in self.order_items:
            removed_quantity = self.order_items.pop(item_lower)
            removed_price = self.menu.get(item_lower, 0) * removed_quantity
            self.total_price -= removed_price

            return (f"✅ Removed **{item_name}** from your order.\n"
                    f"🛒 **Updated Order:** {self.order_items}\n"
                    f"💰 **Updated Total Price: ${self.total_price:.2f}**")
        
        return f"⚠ **{item_name}** is not in your order."

    def update_item(self, order_dict):
        """✅ Updates the quantity of an existing item and adjusts total price."""
        if not isinstance(order_dict, dict):
            return "⚠ Invalid format. Please provide items in dictionary format like: {'item_name': quantity}."

        unavailable_items = []
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
            else:
                unavailable_items.append(item_name)  # Track unavailable items

        if unavailable_items:
            return f"⚠ **The following items are not in your order:** {', '.join(unavailable_items)}.\nPlease add them first before updating."

        return f"✅ **Updated Order:** {self.order_items}\n💰 **Total Price: ${self.total_price:.2f}**"

    
    def estimated_delivery_time(self, order_id):
        """✅ Track estimated delivery time of an order."""
        return self.db.estimated_delivery_time(order_id)
    
    def check_order_status(self, order_id):
        """✅ Retrieve the order status using the stored order ID."""
        return self.db.check_order_status(order_id)

    def cancel_order_before_confirmation(self):
        """✅ Cancels the entire order and resets everything."""
        if not self.order_items:
            return "⚠ You have no active order to cancel."

        self.order_items.clear()
        self.total_price = 0.0

        return "🚫 Your order has been **canceled**. Feel free to start a new order!"

    def cancel_order_after_confirmation(self, order_id):
        """🚫 Cancels the order after confirmation using the stored order ID."""
        return self.db.cancel_order_after_confirmation(order_id)
    
    def replace_item(self, old_item: str, new_item: str):
        """✅ Replace an item in the order while keeping the same quantity and updating price correctly."""
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

        # ✅ If new item already exists, add the quantity instead of replacing it
        if new_item_lower in self.order_items:
            self.order_items[new_item_lower] += quantity
        else:
            self.order_items[new_item_lower] = quantity

        return (f"🔄 Replaced **{old_item}** with **{new_item}**.\n"
                f"🛒 **Updated Order:** {self.order_items}\n"
                f"💰 **Updated Total Price: ${self.total_price:.2f}**")
    def modify_order_after_confirmation(self, order_id, updated_items):
        """✅ Modify an order after confirmation if allowed."""
        try:
            # ✅ Fetch order details from the database
            order_details = self.db.get_order_by_id(order_id)
            if not order_details:
                return f"⚠ No order found with ID {order_id}."

            order_status = order_details["status"]
            order_time_str = order_details["time"]  # Stored as TEXT in SQLite

            # ✅ Convert stored time (string) to datetime object (SQLite stores as "HH:MM:SS")
            order_time = datetime.datetime.strptime(order_time_str, "%H:%M:%S")

            # ✅ Check time limit (Allow modification within 10 minutes)
            current_time = datetime.datetime.now()
            time_diff = (current_time - datetime.datetime.combine(datetime.date.today(), order_time)).total_seconds() / 60

            if time_diff > 10:
                return "⚠ **Your order cannot be modified now. It has been more than 10 minutes.**"
            elif order_status != "Pending":
                return f"⚠ Order {order_id} is already **{order_status}** and cannot be modified."

            # ✅ Validate updated items
            new_total_price = 0.0
            final_order = {}

            for item, quantity in updated_items.items():
                item_lower = item.lower()
                if item_lower in self.menu:
                    final_order[item_lower] = quantity
                    new_total_price += self.menu[item_lower] * quantity
                else:
                    return f"⚠ **{item} is not available in the menu.** Please select a valid item."

            # ✅ Convert updated items to JSON
            updated_items_json = json.dumps(final_order)

            # ✅ Update order in the database
            return self.db.modify_order_after_confirmation(order_id, updated_items_json, new_total_price)

        except Exception as e:
            return f"⚠ Error modifying order: {e}"

# ✅ Example Usage
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
