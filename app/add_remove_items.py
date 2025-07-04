import streamlit as st
import sqlite3
import time  # ⏳ Import time module for delay
from scripts.config import *

# ✅ Function to establish a database connection
def get_connection():
    """🔌 Establish connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

# ✅ Function to check if an item exists
def check_item_exists(item_name):
    """🔍 Check if an item already exists in the menu."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM menu WHERE name = ?"
        cursor.execute(query, (item_name,))
        item = cursor.fetchone()

        conn.close()
        return item is not None  # ✅ Return True if item exists, False otherwise

    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return True  # Assume item exists if an error occurs

# ✅ Function to add a new item
def add_new_item(item_name, price):
    """✅ Insert a new item into the menu if it doesn't exist."""
    if check_item_exists(item_name):
        st.warning(f"⚠ The item **{item_name}** already exists in the menu.", icon="⚠")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO menu (name, price) VALUES (?, ?)"
        cursor.execute(query, (item_name, price))
        conn.commit()
        conn.close()

        st.success(f"✅ **{item_name}** has been added to the menu at **${price:.2f}**! 🎉", icon="🍔")
        return True

    except Exception as e:
        st.error(f"⚠ Error adding item: {e}")
        return False

# ✅ Function to remove an item
def remove_item(item_name):
    """🗑️ Remove an item from the menu."""
    if not check_item_exists(item_name):
        st.warning(f"⚠ The item **{item_name}** does not exist in the menu.", icon="⚠")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM menu WHERE name = ?"
        cursor.execute(query, (item_name,))
        conn.commit()
        conn.close()

        st.success(f"🗑️ **{item_name}** has been successfully removed from the menu.", icon="✅")
        return True

    except Exception as e:
        st.error(f"⚠ Error removing item: {e}")
        return False

# ✅ Function to fetch the menu
def get_menu():
    """📜 Fetch and display all menu items."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT name, price FROM menu ORDER BY name ASC"
        cursor.execute(query)
        items = [{"name": row[0], "price": row[1]} for row in cursor.fetchall()]

        conn.close()
        return items

    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

# ✅ Streamlit UI for Adding/Removing Items
def show_add_remove_items_page():
    """🍽️ Admin Panel - Add or Remove Menu Items"""
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>🔑 Admin Panel</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>📝 Manage Menu Items</h3>", unsafe_allow_html=True)
    st.divider()

    # ✅ Admin Access Check
    if st.session_state["role"] != "admin":
        st.warning("⚠ Access Denied! Only **Admins** can modify menu items.", icon="🚫")
        return

    # ✅ 📜 Display Current Menu
    st.markdown("### 📜 **Current Menu**")
    menu_items = get_menu()

    if not menu_items:
        st.info("ℹ No menu items found.")
    else:
        st.dataframe(menu_items, use_container_width=True, hide_index=True)

    st.divider()

    # ✅ ➕ Add New Item Section
    st.markdown("### ➕ **Add a New Menu Item**")
    col1, col2 = st.columns([2, 1], gap="medium")

    with col1:
        item_name = st.text_input("🔤 Enter Item Name", key="add_item_name", help="Example: Cheeseburger, French Fries")

    with col2:
        price = st.number_input("💰 Enter Price ($)", min_value=0.01, step=0.01, format="%.2f", key="add_item_price")

    if st.button("✅ Add Item", use_container_width=True):
        if item_name and price:
            add_new_item(item_name.strip().capitalize(), price)
            time.sleep(1.2)  # ⏳ Delay for smooth UI transition
            st.rerun()
        else:
            st.warning("⚠ Please enter both **item name** and **price**.", icon="⚠")

    st.divider()

    # ✅ 🗑️ Remove Item Section
    st.markdown("### 🗑️ **Remove an Existing Item**")

    if not menu_items:
        st.info("ℹ No menu items available to remove.")
    else:
        item_list = [item["name"] for item in menu_items]
        selected_item = st.selectbox("📌 Select an item to remove", item_list, key="remove_item_select")

        if st.button("🗑️ Remove Item", use_container_width=True):
            remove_item(selected_item)
            time.sleep(1.2)  # ⏳ Delay for smooth UI transition
            st.rerun()
