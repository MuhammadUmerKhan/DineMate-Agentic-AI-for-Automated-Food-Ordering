import json, datetime
from scripts.db import Database
from scripts.logger import get_logger

# Configure logger
logger = get_logger(__name__)

class OrderHandler:
    def __init__(self):
        """Initialize order handler with menu caching and order storage."""
        self.db = Database()
        self.menu = self.fetch_menu()
        self.order_items = {}
        self.total_price = 0.0
        logger.info("OrderHandler initialized")

    def fetch_menu(self):
        """Fetch and store menu items in memory."""
        try:
            menu = self.db.load_menu()
            if menu:
                menu_dict = {item["name"].lower(): float(item["price"]) for item in menu}
                logger.info(f"Fetched menu with {len(menu_dict)} items")
                return menu_dict
            logger.error("No menu items found")
            return {}
        except Exception as e:
            logger.error(f"Error fetching menu: {e}")
            return {}

    def add_item(self, items_dict):
        """Add items to the order, checking availability and suggesting alternatives."""
        if not isinstance(items_dict, dict):
            logger.error("Invalid items_dict: not a dictionary")
            return "Invalid format. Please provide items as a dictionary."

        response = ""
        unavailable_items = []
        for item, quantity in items_dict.items():
            if not isinstance(quantity, int) or quantity <= 0:
                logger.warning(f"Invalid quantity for {item}: {quantity}")
                unavailable_items.append(item)
                continue
            item_lower = item.lower()
            if item_lower in self.menu:
                self.order_items[item_lower] = self.order_items.get(item_lower, 0) + quantity
                self.total_price += self.menu[item_lower] * quantity
                logger.info(f"Added {quantity}x {item_lower} to order")
                response += f"Added {quantity}x {item}.\n"
            else:
                unavailable_items.append(item)

        if unavailable_items:
            available_items = ", ".join([f"{item.title()}" for item in self.menu.keys()])
            response += f"\nThe following items are unavailable: {', '.join(unavailable_items)}.\nAvailable items: {available_items}.\n"

        logger.info(f"Current order: {self.order_items}, Total: ${self.total_price:.2f}")
        return response + f"\nUpdated Order: {self.order_items}\nTotal Price: ${self.total_price:.2f}"

    def get_order(self):
        """Return the current order stored in memory."""
        logger.info(f"Retrieved order: {self.order_items}")
        return self.order_items if self.order_items else "No items in order."

    def confirm_order(self):
        """Confirm and store the order in the database."""
        if not self.order_items:
            logger.warning("Attempted to confirm empty order")
            return "No items in your order to confirm."

        try:
            order_id = self.db.store_order(self.order_items, self.total_price, "Pending")
            if not order_id:
                logger.error("Failed to store order in database")
                return "Error storing order."

            estimated_time = self.db.estimated_delivery_time(order_id)
            self.order_items = {}
            self.total_price = 0.0
            logger.info(f"Order {order_id} confirmed, reset order_items")
            return f"Your order has been confirmed!\nOrder ID: {order_id}\nEstimated Delivery Time: {estimated_time}"
        except Exception as e:
            logger.error(f"Error confirming order: {e}")
            return f"Error confirming order: {e}"

    def remove_item(self, item_name):
        """Remove an item from the order and update total price."""
        item_lower = item_name.lower()
        if item_lower in self.order_items:
            removed_quantity = self.order_items.pop(item_lower)
            removed_price = self.menu.get(item_lower, 0) * removed_quantity
            self.total_price -= removed_price
            logger.info(f"Removed {item_lower} from order, new total: ${self.total_price:.2f}")
            return f"Removed {item_name} from your order.\nUpdated Order: {self.order_items}\nTotal Price: ${self.total_price:.2f}"
        logger.warning(f"Attempted to remove non-existent item: {item_lower}")
        return f"{item_name} is not in your order."

    def update_item(self, order_dict):
        """Update the quantity of an existing item and adjust total price."""
        if not isinstance(order_dict, dict):
            logger.error("Invalid order_dict: not a dictionary")
            return "Invalid format. Please provide items as a dictionary."

        unavailable_items = []
        for item_name, quantity in order_dict.items():
            if not isinstance(quantity, int) or quantity < 0:
                logger.warning(f"Invalid quantity for {item_name}: {quantity}")
                unavailable_items.append(item_name)
                continue
            item_lower = item_name.lower()
            if item_lower in self.order_items:
                old_quantity = self.order_items[item_lower]
                item_price = self.menu.get(item_lower, 0)
                self.total_price -= old_quantity * item_price
                self.total_price += quantity * item_price
                if quantity == 0:
                    del self.order_items[item_lower]
                else:
                    self.order_items[item_lower] = quantity
                logger.info(f"Updated {item_lower} to quantity {quantity}")
            else:
                unavailable_items.append(item_name)

        if unavailable_items:
            logger.warning(f"Unavailable items: {unavailable_items}")
            return f"The following items are not in your order: {', '.join(unavailable_items)}. Please add them first."
        
        logger.info(f"Updated order: {self.order_items}, Total: ${self.total_price:.2f}")
        return f"Updated Order: {self.order_items}\nTotal Price: ${self.total_price:.2f}"

    def estimated_delivery_time(self, order_id):
        """Track estimated delivery time of an order."""
        logger.info(f"Fetching estimated delivery time for order {order_id}")
        return self.db.estimated_delivery_time(order_id)

    def check_order_status(self, order_id):
        """Retrieve the order status using the stored order ID."""
        logger.info(f"Checking status for order {order_id}")
        return self.db.check_order_status(order_id)

    def cancel_order_before_confirmation(self):
        """Cancel the entire order and reset everything."""
        if not self.order_items:
            logger.warning("Attempted to cancel empty order")
            return "You have no active order to cancel."
        
        self.order_items.clear()
        self.total_price = 0.0
        logger.info("Order canceled before confirmation")
        return "Your order has been canceled. Feel free to start a new order!"

    def cancel_order_after_confirmation(self, order_id):
        """Cancel the order after confirmation using the stored order ID."""
        logger.info(f"Attempting to cancel order {order_id}")
        return self.db.cancel_order_after_confirmation(order_id)

    def replace_item(self, old_item, new_item):
        """Replace an item in the order while keeping the same quantity."""
        old_item_lower = old_item.lower()
        new_item_lower = new_item.lower()
        if old_item_lower not in self.order_items:
            logger.warning(f"Attempted to replace non-existent item: {old_item_lower}")
            return f"{old_item} is not in your order."
        if new_item_lower not in self.menu:
            logger.warning(f"Replacement item not in menu: {new_item_lower}")
            return f"{new_item} is not available in the menu."

        quantity = self.order_items.pop(old_item_lower)
        old_price = self.menu.get(old_item_lower, 0) * quantity
        new_price = self.menu.get(new_item_lower, 0) * quantity
        self.total_price = self.total_price - old_price + new_price
        self.order_items[new_item_lower] = self.order_items.get(new_item_lower, 0) + quantity
        logger.info(f"Replaced {old_item_lower} with {new_item_lower}, new total: ${self.total_price:.2f}")
        return f"Replaced {old_item} with {new_item}.\nUpdated Order: {self.order_items}\nTotal Price: ${self.total_price:.2f}"

    def modify_order_after_confirmation(self, order_id, updated_items):
        """Modify an order after confirmation if allowed."""
        try:
            order_details = self.db.get_order_by_id(order_id)
            if not order_details:
                logger.warning(f"No order found with ID {order_id}")
                return f"No order found with ID {order_id}"

            order_status = order_details["status"]
            order_date = datetime.datetime.strptime(order_details["date"], "%Y-%m-%d").date()
            order_time = datetime.datetime.strptime(order_details["time"], "%I:%M:%S %p").time()
            order_datetime = datetime.datetime.combine(order_date, order_time)
            time_diff = (datetime.datetime.now() - order_datetime).total_seconds() / 60

            if time_diff > 10:
                logger.warning(f"Order {order_id} modification rejected: past 10-minute window")
                return "Your order cannot be modified now. It has been more than 10 minutes."
            if order_status != "Pending":
                logger.warning(f"Order {order_id} modification rejected: status is {order_status}")
                return f"Order {order_id} is already {order_status} and cannot be modified."

            new_total_price = 0.0
            final_order = {}
            for item, quantity in updated_items.items():
                item_lower = item.lower()
                if item_lower in self.menu:
                    final_order[item_lower] = quantity
                    new_total_price += self.menu[item_lower] * quantity
                else:
                    logger.warning(f"Invalid item in modified order: {item_lower}")
                    return f"{item} is not available in the menu."

            updated_items_json = json.dumps(final_order)
            result = self.db.modify_order_after_confirmation(order_id, updated_items_json, new_total_price)
            logger.info(f"Order {order_id} modified successfully")
            return result
        except Exception as e:
            logger.error(f"Error modifying order {order_id}: {e}")
            return f"Error modifying order: {e}"