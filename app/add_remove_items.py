import streamlit as st
import mysql.connector
from config import DB_CONFIG  # ✅ Database connection configuration
import time  # ⏳ Import time module for delay

def check_item_exists(item_name):
    """✅ Check if an item already exists in the menu."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM menu WHERE name = %s"
        cursor.execute(query, (item_name,))
        item = cursor.fetchone()

        cursor.close()
        conn.close()

        return item is not None  # ✅ Return True if item exists, False otherwise

    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return True  # Assume item exists if an error occurs

def add_new_item(item_name, price):
    """✅ Insert a new item into the menu if it doesn't exist."""
    if check_item_exists(item_name):
        st.warning(f"⚠ The item **{item_name}** already exists in the menu.")
        return False

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "INSERT INTO menu (name, price) VALUES (%s, %s)"
        cursor.execute(query, (item_name, price))
        conn.commit()

        cursor.close()
        conn.close()

        st.success(f"✅ **{item_name}** added to the menu at **${price:.2f}**!")
        return True

    except Exception as e:
        st.error(f"⚠ Error adding item: {e}")
        return False

def remove_item(item_name):
    """✅ Remove an item from the menu."""
    if not check_item_exists(item_name):
        st.warning(f"⚠ The item **{item_name}** does not exist in the menu.")
        return False

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM menu WHERE name = %s"
        cursor.execute(query, (item_name,))
        conn.commit()

        cursor.close()
        conn.close()

        st.success(f"🗑️ **{item_name}** removed from the menu.")
        return True

    except Exception as e:
        st.error(f"⚠ Error removing item: {e}")
        return False

def get_menu():
    """✅ Fetch and display all menu items."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT name, price FROM menu ORDER BY name ASC"
        cursor.execute(query)
        items = cursor.fetchall()

        cursor.close()
        conn.close()

        return items

    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

# ✅ Streamlit UI for Adding/Removing Items
def show_add_remove_items_page():
    """✅ Page for adding and removing menu items."""
    st.title("🔑 Admin Panel - Manage Menu Items")
    st.write("### ➕ Add or 🗑️ Remove food items from the menu.")

    if st.session_state["role"] != "admin":
        st.warning("⚠ Access Denied. Only admins can modify menu items.")
        return

    st.markdown("---")
    # ✅ Add New Item Section
    st.subheader("➕ Add New Item")
    item_name = st.text_input("🍔 Enter Item Name", key="add_item_name")
    price = st.number_input("💰 Enter Price ($)", min_value=0.01, step=0.01, format="%.2f", key="add_item_price")

    if st.button("✅ Add Item"):
        if item_name and price:
            add_new_item(item_name.strip().capitalize(), price)
            time.sleep(1.2)  # ⏳ Delay for 2 seconds
            st.rerun()
        else:
            st.warning("⚠ Please enter both **item name** and **price**.")

    st.markdown("---")
    # ✅ Remove Item Section
    st.subheader("🗑️ Remove Existing Item")
    menu_items = get_menu()
    
    if not menu_items:
        st.info("ℹ No menu items available to remove.")
    else:
        item_list = [item["name"] for item in menu_items]
        selected_item = st.selectbox("📌 Select an item to remove", item_list, key="remove_item_select")

        if st.button("🗑️ Remove Item"):
            remove_item(selected_item)
            time.sleep(1.2)  # ⏳ Delay for 2 seconds
            st.rerun()

    # ✅ Display Current Menu
    st.write("### 📜 Current Menu")
    if not menu_items:
        st.info("ℹ No menu items found.")
    else:
        st.dataframe(menu_items, use_container_width=True, width=400, hide_index=False)
