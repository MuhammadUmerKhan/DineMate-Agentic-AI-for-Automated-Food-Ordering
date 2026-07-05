"""Utility helpers for order validation and price recomputation."""

import json
from typing import Any

from scripts.db import AsyncDatabase
from scripts.logger import get_logger

logger = get_logger(__name__)


async def fetch_price_lookup(items: list[str]) -> dict:
    """Fetch prices for a list of items directly from the database.

    Args:
        items: Item names to look up in the menu.

    Returns:
        A dictionary mapping each item name to its price, or None for unknown items.
    """
    async with AsyncDatabase() as db:
        full_menu = await db.load_menu()
        if not full_menu:
            return {}

        prices = {}
        for item in set(items):
            lower_item = str(item).lower()
            matching_key = next((k for k in full_menu if str(k).lower() == lower_item), None)
            if matching_key:
                prices[matching_key] = full_menu[matching_key]
            else:
                prices[item] = None

        return prices


def coerce_order_payload(order_details: Any) -> tuple[dict | None, str | None]:
    """Normalize order payloads from either a JSON string or a structured object.

    Args:
        order_details: Either a JSON string or a dictionary payload.

    Returns:
        A tuple of (parsed_payload, error_message).
    """
    if isinstance(order_details, str):
        try:
            parsed = json.loads(order_details)
        except json.JSONDecodeError:
            return None, "Invalid JSON."
    elif isinstance(order_details, dict):
        parsed = order_details
    else:
        return None, "Invalid order details."

    if not isinstance(parsed, dict):
        return None, "Invalid order details."

    return parsed, None


async def recompute_total_price(items: dict) -> tuple[float | None, str | None]:
    """Recompute an order total from current menu prices and reject invalid items.

    Args:
        items: Mapping of item names to quantities.

    Returns:
        A tuple of (computed_total, error_message).
    """
    if not items:
        return None, "No items."

    total_price = 0.0
    for item_name, quantity in items.items():
        price_lookup = await fetch_price_lookup([item_name])

        price = None
        normalized_item = str(item_name).lower()
        if item_name in price_lookup:
            price = price_lookup[item_name]
        else:
            for menu_item, menu_price in price_lookup.items():
                if str(menu_item).lower() == normalized_item:
                    price = menu_price
                    break

        if price is None:
            for menu_item, menu_price in price_lookup.items():
                if str(menu_item).lower() == normalized_item:
                    price = menu_price
                    break

        if price is None:
            return None, f"Price unavailable for item '{item_name}'."

        try:
            price_value = float(price)
        except (TypeError, ValueError):
            return None, f"Invalid price for item '{item_name}'."

        try:
            quantity_value = float(quantity)
        except (TypeError, ValueError):
            return None, f"Invalid quantity for item '{item_name}'."

        total_price += price_value * quantity_value

    return total_price, None
