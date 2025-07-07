"""
# DineMate Order Handler

This module handles in-memory order processing for the DineMate foodbot.

Dependencies:
- json: For JSON handling.
- db: For database operations.
- logger: For logging.
"""

import json
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
        logger.info("OrderHandler initialized")

    def fetch_menu(self) -> Dict[str, float]:
        """Fetch and cache menu items.

        Returns:
            Dict[str, float]: Menu items and prices.
        """
        try:
            menu = self.db.load_menu()
            menu_dict = {item["name"].lower(): float(item["price"]) for item in menu} if menu else {}
            logger.info(f"Fetched menu with {len(menu_dict)} items")
            return menu_dict
        except Exception as e:
            logger.error({"error": str(e)})
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
            logger.error({"invalid_input": type(items_dict)})
            return "Invalid item format."

        response = []
        unavailable = []
        for item, quantity in items_dict.items():
            if not isinstance(quantity, int) or quantity <= 0:
                logger.warning({"invalid_quantity": {"item": item, "quantity": quantity}})
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
            available = ", ".join(self.menu.keys())
            response.append(f"Unavailable items: {', '.join(unavailable)}. Available: {available}.")

        logger.info({"order_items": self.order_items, "total_price": self.total_price})
        return "\n".join(response) + f"\nOrder: {self.order_items}, Total: ${self.total_price:.2f}"

    def get_order(self) -> Union[Dict[str, int], str]:
        """Return current order.

        Returns:
            Union[Dict[str, int], str]: Order items or message if empty.
        """
        logger.info({"order_items": self.order_items})
        return self.order_items if self.order_items else "No items in order."

    def confirm_order(self) -> str:
        """Confirm and store order in database.

        Returns:
            str: Confirmation message.
        """
        if not self.order_items:
            logger.warning("Empty order")
            return "No items to confirm."

        try:
            order_id = self.db.store_order_db(self.order_items, self.total_price)
            if not order_id:
                logger.error("Failed to store order")
                return "Error storing order."
            self.order_items = {}
            self.total_price = 0.0
            logger.info({"order_id": order_id, "status": "confirmed"})
            return f"Order confirmed! ID: {order_id}, Delivery in 40 minutes."
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
            logger.warning({"item": item_lower, "status": "not_in_order"})
            return f"{item_name} not in order."
        quantity = self.order_items.pop(item_lower)
        self.total_price -= self.menu.get(item_lower, 0) * quantity
        logger.info({"order_items": self.order_items, "total_price": self.total_price})
        return f"Removed {item_name}. Order: {self.order_items}, Total: ${self.total_price:.2f}"

    def update_item(self, order_dict: Dict[str, int]) -> str:
        """Update item quantities.

        Args:
            order_dict (Dict[str, int]): Items and new quantities.

        Returns:
            str: Confirmation message.
        """
        if not isinstance(order_dict, dict):
            logger.error({"invalid_input": type(order_dict)})
            return "Invalid item format."

        unavailable = []
        for item, quantity in order_dict.items():
            if not isinstance(quantity, int) or quantity < 0:
                logger.warning({"invalid_quantity": {"item": item, "quantity": quantity}})
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
            logger.warning({"unavailable_items": unavailable})
            return f"Not in order: {', '.join(unavailable)}. Add them first."
        
        logger.info({"order_items": self.order_items, "total_price": self.total_price})
        return f"Order updated: {self.order_items}, Total: ${self.total_price:.2f}"

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
            logger.warning({"item": old_item_lower, "status": "not_in_order"})
            return f"{old_item} not in order."
        if new_item_lower not in self.menu:
            logger.warning({"item": new_item_lower, "status": "not_in_menu"})
            return f"{new_item} not in menu."

        quantity = self.order_items.pop(old_item_lower)
        old_price = self.menu.get(old_item_lower, 0) * quantity
        new_price = self.menu.get(new_item_lower, 0) * quantity
        self.total_price = self.total_price - old_price + new_price
        self.order_items[new_item_lower] = quantity
        logger.info({"order_items": self.order_items, "total_price": self.total_price})
        return f"Replaced {old_item} with {new_item}. Order: {self.order_items}, Total: ${self.total_price:.2f}"