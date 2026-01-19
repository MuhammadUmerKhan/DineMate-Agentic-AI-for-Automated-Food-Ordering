"""
# DineMate Order Handler

This module handles in-memory order processing for the DineMate foodbot.

Dependencies:
- json: For JSON handling.
- db: For database operations.
- logger: For logging.
"""

from typing import Dict, Union
from scripts.db import Database
from scripts.logger import get_logger

logger = get_logger(__name__)

class OrderHandler:
    def __init__(self):
        """Initialize order handler with menu caching."""
        self.db = Database()
        self.menu = self.fetch_menu()
        self.order_items: Dict[str, int] = {}
        self.total_price: float = 0.0
        logger.info("🍽️ OrderHandler initialized")

    def fetch_menu(self) -> Dict[str, float]:
        """Fetch and cache menu items.

        Returns:
            Dict[str, float]: Menu items and prices.
        """
        try:
            menu = self.db.load_menu()
            # load_menu() returns a dict {name: price}, convert keys to lowercase
            menu_dict = {name.lower(): float(price) for name, price in menu.items()} if menu else {}
            logger.info("🍔 Fetched menu")
            return menu_dict
        except Exception as e:
            logger.error({"error": str(e), "message": "❌ Menu fetch failed"})
            return {}
        finally:
            self.db.close_connection()

    def add_item(self, items_dict: Dict[str, int]) -> str:
        """Add items to the order.

        Args:
            items_dict (Dict[str, int]): Items and quantities.

        Returns:
            str: Confirmation message.
        """
        if not isinstance(items_dict, dict):
            logger.error("❌ Invalid item format")
            return "Invalid format."

        response = []
        unavailable = []
        for item, quantity in items_dict.items():
            if not isinstance(quantity, int) or quantity <= 0:
                unavailable.append(item)
                continue
            item_lower = item.lower()
            if item_lower in self.menu:
                self.order_items[item_lower] = self.order_items.get(item_lower, 0) + quantity
                self.total_price += self.menu[item_lower] * quantity
                response.append(f"Added {quantity}x {item}")
            else:
                unavailable.append(item)

        if unavailable:
            response.append(f"Unavailable: {', '.join(unavailable)}. Available: {', '.join(self.menu.keys())}.")

        logger.info("🛒 Order updated")
        return "\n".join(response) + f"\nTotal: ${self.total_price:.2f}"

    def get_order(self) -> Union[Dict[str, int], str]:
        """Return current order.

        Returns:
            Union[Dict[str, int], str]: Order items or message if empty.
        """
        logger.info("📋 Fetching order")
        return self.order_items if self.order_items else "No items."

    def confirm_order(self) -> str:
        """Confirm and store order in database.

        Returns:
            str: Confirmation message.
        """
        if not self.order_items:
            logger.warning("⚠️ Empty order")
            return "No items to confirm."

        try:
            order_id = self.db.store_order_db(self.order_items, self.total_price)
            if not order_id:
                logger.error("❌ Order store failed")
                return "Error storing."
            self.order_items = {}
            self.total_price = 0.0
            logger.info("✅ Order confirmed")
            return f"Order {order_id} confirmed. Delivery in 40 min."
        finally:
            self.db.close_connection()

    def remove_item(self, item_name: str) -> str:
        """Remove an item from the order.

        Args:
            item_name (str): Item to remove.

        Returns:
            str: Confirmation message.
        """
        item_lower = item_name.lower()
        if item_lower not in self.order_items:
            logger.warning("⚠️ Item not in order")
            return f"{item_name} not found."
        quantity = self.order_items.pop(item_lower)
        self.total_price -= self.menu.get(item_lower, 0) * quantity
        logger.info("🗑️ Item removed")
        return f"Removed {item_name}. Total: ${self.total_price:.2f}"

    def update_item(self, order_dict: Dict[str, int]) -> str:
        """Update item quantities.

        Args:
            order_dict (Dict[str, int]): Items and new quantities.

        Returns:
            str: Confirmation message.
        """
        if not isinstance(order_dict, dict):
            logger.error("❌ Invalid format")
            return "Invalid format."

        unavailable = []
        for item, quantity in order_dict.items():
            if not isinstance(quantity, int) or quantity < 0:
                unavailable.append(item)
                continue
            item_lower = item.lower()
            if item_lower in self.order_items:
                old_quantity = self.order_items[item_lower]
                item_price = self.menu.get(item_lower, 0)
                self.total_price -= old_quantity * item_price
                self.total_price += quantity * item_price
                if quantity == 0:
                    del self.order_items[item_lower]
                else:
                    self.order_items[item_lower] = quantity
            else:
                unavailable.append(item)

        if unavailable:
            logger.warning("⚠️ Items not in order")
            return f"Not in order: {', '.join(unavailable)}."

        logger.info("🔄 Order updated")
        return f"Updated: {self.order_items}, Total: ${self.total_price:.2f}"

    def replace_item(self, old_item: str, new_item: str) -> str:
        """Replace an item in the order.

        Args:
            old_item (str): Item to replace.
            new_item (str): New item.

        Returns:
            str: Confirmation message.
        """
        old_item_lower = old_item.lower()
        new_item_lower = new_item.lower()
        if old_item_lower not in self.order_items:
            logger.warning("⚠️ Item not in order")
            return f"{old_item} not found."
        if new_item_lower not in self.menu:
            logger.warning("⚠️ Item not in menu")
            return f"{new_item} not available."

        quantity = self.order_items.pop(old_item_lower)
        old_price = self.menu.get(old_item_lower, 0) * quantity
        new_price = self.menu.get(new_item_lower, 0) * quantity
        self.total_price = self.total_price - old_price + new_price
        self.order_items[new_item_lower] = quantity
        logger.info("🔄 Item replaced")
        return f"Replaced {old_item} with {new_item}. Total: ${self.total_price:.2f}"