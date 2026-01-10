"""
# DineMate Price Management 💰

This module allows admins to update menu item prices.

Dependencies:
- streamlit: For UI rendering 📺.
- pandas: For data display 📊.
- db: For database operations 🗄️.
- logger: For structured logging 📜.
"""

import streamlit as st
import pandas as pd, time
from scripts.db import Database
from scripts.logger import get_logger
from typing import List, Dict

logger = get_logger(__name__)

def get_menu_items() -> List[Dict]:
    """📜 Fetch all menu items with prices.

    Returns:
        List[Dict]: List of menu items with name and price.
    """
    try:
        db = Database()
        db.cursor.execute("SELECT name, price FROM menu")
        items = [{"name": row["name"], "price": float(row["price"])} for row in db.cursor.fetchall()]
        logger.info({"count": len(items), "message": "Fetched menu items"})
        return items
    except Exception as e:
        logger.error({"error": str(e), "message": "Failed to fetch menu items"})
        st.error(f"⚠ Database error: {e}")
        return []
    finally:
        db.close_connection()

def update_item_price(item_name: str, new_price: float) -> None:
    """✅ Update the price of a menu item.

    Args:
        item_name (str): Name of the item.
        new_price (float): New price.
    """
    logger.info({"item_name": item_name, "new_price": new_price, "message": "Updating item price"})
    if new_price <= 0:
        st.warning("⚠ Price must be positive.")
        logger.warning({"item_name": item_name, "new_price": new_price, "message": "Invalid price"})
        return

    try:
        db = Database()
        db.cursor.execute("UPDATE menu SET price = ? WHERE name = ?", (new_price, item_name))
        db.connection.commit()
        st.success(f"✅ Price for {item_name} updated to ${new_price:.2f}! 🎉")
        logger.info({"item_name": item_name, "new_price": new_price, "message": "Price updated"})
    except Exception as e:
        logger.error({"error": str(e), "item_name": item_name, "new_price": new_price})
        st.error(f"⚠ Error updating price: {e}")
    finally:
        db.close_connection()

def show_price_update_page() -> None:
    """💰 Admin panel for updating menu prices."""
    
    st.markdown(
        "<div class='header'><h1>🛡️ Update Prices</h1><p style='color: #E8ECEF;'>💰 Admin panel for menu price updates</p></div>",
        unsafe_allow_html=True
    )
    
    if st.session_state.get("role") != "admin":
        st.warning("⚠ Only admins can update prices.", icon="🚫")
        logger.warning({"role": st.session_state.get("role"), "message": "Access denied"})
        return

    with st.spinner("⏳ Loading menu..."):
        menu_items = get_menu_items()

    if not menu_items:
        st.info("✅ No menu items found.")
    else:
        st.write("### 📜 Current Menu & Prices")
        df_menu = pd.DataFrame(menu_items).rename(columns={"name": "🍲 Item Name", "price": "💰 Price ($)"})
        st.dataframe(df_menu, width="stretch")

    st.divider()
    st.write("### ✏️ Modify Item Price")
    col1, col2 = st.columns([2, 2])
    with col1:
        item_dict = {item["name"]: item["price"] for item in menu_items}
        selected_item = st.selectbox("📌 Select Item", list(item_dict.keys()))
        current_price = item_dict.get(selected_item, 0.0)
    with col2:
        new_price = st.number_input("💵 New Price ($)", min_value=0.01, value=current_price, step=0.01, format="%.2f")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✔ Update Price", width="stretch"):
            with st.spinner("⏳ Updating price..."):
                update_item_price(selected_item, new_price)
                time.sleep(0.5)
                st.rerun()
    with col2:
        if st.button("🔄 Reset", width="stretch"):
            st.rerun()