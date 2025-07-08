"""
# DineMate Menu Management 🍽️

This module allows admins to add or remove menu items.

Dependencies:
- streamlit: For UI rendering 📺.
- db: For database operations 🗄️.
- logger: For structured logging 📜.
"""

import streamlit as st
import pandas as pd
from scripts.db import Database
from scripts.logger import get_logger
from scripts.config import STATIC_CSS_PATH
from typing import List, Dict, Optional
import time

logger = get_logger(__name__)

# ✅ Load centralized CSS
try:
    with open(STATIC_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

def check_item_exists(item_name: str) -> bool:
    try:
        db = Database()
        db.cursor.execute("SELECT 1 FROM menu WHERE name = ?", (item_name,))
        exists = db.cursor.fetchone() is not None
        logger.info({"item_name": item_name, "exists": exists, "message": "Checked item existence"})
        return exists
    except Exception as e:
        logger.error({"error": str(e), "item_name": item_name})
        st.error(f"⚠ Database error: {e}")
        return True
    finally:
        db.close_connection()

def add_new_item(item_name: str, price: float) -> bool:
    logger.info({"item_name": item_name, "price": price, "message": "Adding new item"})
    if check_item_exists(item_name):
        st.warning(f"⚠ Item {item_name} already exists.", icon="⚠")
        logger.warning({"item_name": item_name, "message": "Item already exists"})
        return False
    if not item_name or price <= 0:
        st.warning("⚠ Invalid item name or price.", icon="⚠")
        logger.warning({"item_name": item_name, "price": price, "message": "Invalid input"})
        return False

    try:
        db = Database()
        db.cursor.execute("INSERT INTO menu (name, price) VALUES (?, ?)", (item_name, price))
        db.connection.commit()
        st.success(f"✅ {item_name} added at ${price:.2f}! 🎉")
        logger.info({"item_name": item_name, "price": price, "message": "Item added"})
        return True
    except Exception as e:
        logger.error({"error": str(e), "item_name": item_name, "price": price})
        st.error(f"⚠ Error adding item: {e}")
        return False
    finally:
        db.close_connection()

def remove_item(item_name: str) -> bool:
    logger.info({"item_name": item_name, "message": "Removing item"})
    if not check_item_exists(item_name):
        st.warning(f"⚠ Item {item_name} does not exist.", icon="⚠")
        logger.warning({"item_name": item_name, "message": "Item does not exist"})
        return False

    try:
        db = Database()
        db.cursor.execute("DELETE FROM menu WHERE name = ?", (item_name,))
        db.connection.commit()
        st.success(f"🗑️ {item_name} removed successfully! ✅")
        logger.info({"item_name": item_name, "message": "Item removed"})
        return True
    except Exception as e:
        logger.error({"error": str(e), "item_name": item_name})
        st.error(f"⚠ Error removing item: {e}")
        return False
    finally:
        db.close_connection()

def get_menu() -> List[Dict]:
    try:
        db = Database()
        db.cursor.execute("SELECT name, price FROM menu ORDER BY name")
        items = [{"name": row["name"], "price": float(row["price"])} for row in db.cursor.fetchall()]
        logger.info({"count": len(items), "message": "Fetched menu items"})
        return items
    except Exception as e:
        logger.error({"error": str(e), "message": "Failed to fetch menu"})
        st.error(f"⚠ Database error: {e}")
        return []
    finally:
        db.close_connection()

def show_add_remove_items_page() -> None:
    if st.session_state.get("role") != "admin":
        st.markdown(
            "<div class='warning-container'><h3 style='color: #EF0606;'>⚠ Access Denied</h3><p>Only admins can modify menu items.</p></div>",
            unsafe_allow_html=True
        )
        logger.warning({"role": st.session_state.get("role"), "message": "Access denied"})
        return

    st.markdown(
        "<div class='header'><h1>➕ Add/Remove Items</h1><p style='color: #E8ECEF;'>🍽️ Manage menu items</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    # 📜 Current Menu
    with st.spinner("⏳ Loading menu..."):
        menu_items = get_menu()
    if not menu_items:
        st.info("ℹ No menu items found.")
    else:
        st.markdown("### 📜 Current Menu")
        st.dataframe(
            pd.DataFrame(menu_items).rename(columns={"name": "🍲 Item Name", "price": "💰 Price ($)"}),
            use_container_width=True, hide_index=True
        )

    st.divider()

    # ➕ Add Item
    st.markdown("### ➕ Add New Menu Item")
    col1, col2 = st.columns([2, 1], gap="medium")
    with col1:
        item_name = st.text_input("🔤 Item Name", key="add_item_name", help="e.g., Cheeseburger", placeholder="Enter item name")
    with col2:
        price = st.number_input("💰 Price ($)", min_value=0.01, step=0.01, format="%.2f", key="add_item_price")

    if st.button("✅ Add Item", use_container_width=True):
        with st.spinner("⏳ Adding item..."):
            add_new_item(item_name.strip().capitalize(), price)
            time.sleep(0.5)
            st.rerun()

    st.divider()

    # 🗑️ Remove Item
    st.markdown("### 🗑️ Remove Menu Item")
    if not menu_items:
        st.info("ℹ No items to remove.")
    else:
        item_list = [item["name"] for item in menu_items]
        selected_item = st.selectbox("📌 Select Item to Remove", item_list, key="remove_item_select", help="Choose an item to remove")
        if st.button("🗑️ Remove Item", use_container_width=True):
            with st.spinner("⏳ Removing item..."):
                remove_item(selected_item)
                time.sleep(0.5)
                st.rerun()