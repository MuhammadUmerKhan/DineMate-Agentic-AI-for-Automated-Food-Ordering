import streamlit as st
import mysql.connector
from config import DB_CONFIG  # ✅ Database connection configuration
import time  # ⏳ Import time module for delay

# ✅ Function to check if item exists
def check_item_exists(item_name):
    """🔍 Check if an item already exists in the menu."""
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

# ✅ Function to add a new item
def add_new_item(item_name, price):
    """✅ Insert a new item into the menu if it doesn't exist."""
    if check_item_exists(item_name):
        st.warning(f"⚠ The item **{item_name}** already exists in the menu.", icon="⚠")
        return False

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "INSERT INTO menu (name, price) VALUES (%s, %s)"
        cursor.execute(query, (item_name, price))
        conn.commit()

        cursor.close()
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
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM menu WHERE name = %s"
        cursor.execute(query, (item_name,))
        conn.commit()

        cursor.close()
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
    """🍽️ Admin Panel - Add or Remove Menu Items"""
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>🔑 Admin Panel</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>📝 Add or Remove Food Items</h3>", unsafe_allow_html=True)

    # ✅ Admin Access Check
    if st.session_state["role"] != "admin":
        st.warning("⚠ Access Denied! Only **Admins** can modify menu items.", icon="🚫")
        return

    # ✅ Layout: Two Sections (Add & Remove)
    tab1, tab2 = st.tabs(["➕ **Add Item**", "🗑️ **Remove Item**"])

    # ✅ ➕ Add New Item Section
    with tab1:
        st.markdown("### 🍔 **Add a New Menu Item**")
        item_name = st.text_input("🔤 Enter Item Name", key="add_item_name", help="Example: Cheeseburger, French Fries")
        price = st.number_input("💰 Enter Price ($)", min_value=0.01, step=0.01, format="%.2f", key="add_item_price")

        # ✅ Button in Center
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Add Item", use_container_width=True):
                if item_name and price:
                    add_new_item(item_name.strip().capitalize(), price)
                    time.sleep(1.2)  # ⏳ Delay for 2 seconds
                    st.rerun()
                else:
                    st.warning("⚠ Please enter both **item name** and **price**.", icon="⚠")

    # ✅ 🗑️ Remove Item Section
    with tab2:
        st.markdown("### 🗑️ **Remove an Existing Item**")
        menu_items = get_menu()
        
        if not menu_items:
            st.info("ℹ No menu items available to remove.")
        else:
            item_list = [item["name"] for item in menu_items]
            selected_item = st.selectbox("📌 Select an item to remove", item_list, key="remove_item_select")

            # ✅ Button in Center
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🗑️ Remove Item", use_container_width=True):
                    remove_item(selected_item)
                    time.sleep(1.2)  # ⏳ Delay for 2 seconds
                    st.rerun()

    st.divider()

    # ✅ 📜 Display Current Menu
    st.markdown("### 📜 **Current Menu**")
    if not menu_items:
        st.info("ℹ No menu items found.")
    else:
        st.dataframe(menu_items, use_container_width=True, hide_index=True)
