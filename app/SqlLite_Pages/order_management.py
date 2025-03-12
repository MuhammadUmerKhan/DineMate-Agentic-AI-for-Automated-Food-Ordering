import streamlit as st
import json
import sqlite3
import pandas as pd
import time
import re
from order.order_handler_lite import OrderHandler
from database.SQLLITE_db import Database
from config import *

# ✅ Initialize the order handler
order_handler = OrderHandler()

def get_connection():
    """🔌 Establish connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def get_all_orders():
    """✅ Fetch all customer orders from the database sorted by latest date & time."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, items, total_price, status, time, date 
        FROM orders 
        ORDER BY date DESC, time DESC
        """
        cursor.execute(query)
        orders = [{"id": row[0], "items": row[1], "total_price": row[2], "status": row[3], "time": row[4], "date": row[5]} for row in cursor.fetchall()]

        conn.close()
        return orders
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

def update_order_item(order_id, new_items):
    """✅ Update order items & recalculate price while warning about unavailable items."""
    try:
        try:
            new_items_dict = json.loads(new_items)
        except json.JSONDecodeError:
            st.error("⚠ Invalid JSON format. Use `{'item_name': quantity}` format.")
            return

        valid_items = {}
        warnings = []

        for item, quantity in new_items_dict.items():
            if item.lower() in order_handler.menu:
                valid_items[item] = quantity
            else:
                warnings.append(f"⚠ **{item}** is not available in the menu.")

        if warnings:
            for warning in warnings:
                st.warning(warning)

        if valid_items:
            response = order_handler.modify_order_after_confirmation(order_id, valid_items)
            if "✅" in response:
                st.success(response)
            else:
                st.error(response)

    except Exception as e:
        st.error(f"⚠ Error updating order: {e}")

def update_order_status(order_id, new_status):
    """✅ Update the status of an order."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE orders SET status = ? WHERE id = ?"
        cursor.execute(query, (new_status, order_id))
        conn.commit()
        conn.close()
        
        st.success(f"✅ Order {order_id} updated to **{new_status}**! 🎉", icon="🔄")

    except Exception as e:
        st.error(f"⚠ Error updating order: {e}")

def cancel_order(order_id):
    """✅ Cancel an order."""
    response = order_handler.db.cancel_order_after_confirmation(order_id)

    if "✅" in response:
        st.success(response)
    else:
        st.warning(response)
        
def add_new_order(items_input):
    """✅ Adds a new order with the next available ID."""
    try:
        # ✅ Extract items & quantities from input
        extracted_items = extract_items_quantity(items_input)
        
        if not extracted_items:
            st.warning("⚠ No valid items found. Please enter items like '2 burgers, 3 cokes'.")
            return

        # ✅ Initialize database connection
        db = Database()  # ✅ Create an instance of Database
        new_order_id = db.get_max_id()  # ✅ Call the method on instance

        if new_order_id is None:
            return

        # ✅ Calculate total price
        total_price = sum(order_handler.menu[item] * qty for item, qty in extracted_items.items() if item in order_handler.menu)

        # ✅ Convert items to JSON format
        order_json = json.dumps(extracted_items)

        # ✅ Get current date & time
        now = time.strftime("%Y-%m-%d"), time.strftime("%I:%M:%S %p")

        # ✅ Store order in the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (id, items, total_price, status, date, time) VALUES (?, ?, ?, ?, ?, ?);",
            (new_order_id, order_json, total_price, "Pending", now[0], now[1])
        )
        conn.commit()
        conn.close()

        st.success(f"✅ New order (ID: {new_order_id}) added successfully!")
    
    except Exception as e:
        st.error(f"⚠ Error adding new order: {e}")

def extract_items_quantity(user_input):
    """✅ Extracts food items and quantities from user input and returns a dictionary."""
    
    # ✅ Define a regex pattern to correctly extract (quantity + item) pairs
    pattern = r'(\d+)\s+([a-zA-Z\s-]+)'

    # ✅ Find all matches in the user input
    matches = re.findall(pattern, user_input)

    # ✅ Create a dictionary to store extracted items
    order_dict = {}

    for quantity, item in matches:
        item = item.strip().lower()  # Convert item name to lowercase
        quantity = int(quantity)  # Convert quantity to integer
        
        # ✅ Handle duplicate items (sum their quantities)
        if item in order_dict:
            order_dict[item] += quantity
        else:
            order_dict[item] = quantity

    return order_dict if order_dict else None  # ✅ Return None if no valid items found

# ✅ Streamlit UI for Order Management
# ✅ Streamlit UI for Order Management
def show_order_management():
    """✅ Customer Support Panel to manage orders (Modify, Cancel, Update Status)."""
    st.markdown("<h1 style='text-align: center;'>📦 Order Management - Customer Support</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>🔄 Modify, cancel, update orders, or add a new order.</p>", unsafe_allow_html=True)
    st.divider()

    orders = get_all_orders()

    if not orders:
        st.info("✅ No orders found.")
        return

    # ✅ Show orders in a table
    st.write("### 📝 **Customer Orders Overview**")
    df = pd.DataFrame(orders)
    df.rename(columns={"id": "📦 Order ID", "items": "🍲 Ordered Items", "total_price": "💰 Total Price ($)", "status": "🟢 Order Status", "time": "🕰️ Order Time", "date": "🗓️ Date"}, inplace=True)
    st.dataframe(df, use_container_width=True)
    st.divider()

    # ✅ **Order ID Selection (Always at the Top)**
    st.markdown("### 🔍 **Select Order to Modify**")
    selected_order = st.selectbox("📌 Select an Order ID", [order["id"] for order in orders])

    st.divider()

    # ✅ **Modify Order Section**
    st.markdown("### ✏️ **Modify Order Items**")
    new_items = st.text_area("📝 Modify Items (e.g., '2 burgers, 3 cokes')", height=68, key="modify_items")

    if st.button("✔ Update Items", use_container_width=True):
        extracted_items = extract_items_quantity(new_items)
        if extracted_items:
            update_order_item(selected_order, json.dumps(extracted_items))
            time.sleep(1.2)
            st.rerun()
        else:
            st.warning("⚠ No valid items found. Please enter items in format: '2 burgers, 3 cokes'.")

    st.divider()

    # ✅ **Update Order Status Section**
    st.markdown("### 🔄 **Update Order Status**")
    new_status = st.selectbox(
        "🔄 Select New Status",
        ["Pending", "In Process", "Preparing", "Ready", "Completed", "Canceled"],
        key="update_status"
    )
    if st.button("✅ Update Status", use_container_width=True):
        update_order_status(selected_order, new_status)
        time.sleep(1.2)
        st.rerun()

    st.divider()

    # ✅ **Add New Order Section**
    st.markdown("### ➕ **Add New Order**")

    new_order_items = st.text_input("📝 Enter New Order (e.g., '2 burgers, 3 cokes')")

    if st.button("➕ Add Order", use_container_width=True):
        add_new_order(new_order_items)
        time.sleep(1.2)
        st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center;'>📞 Need help? Customer support is here for you! 🤝</p>", unsafe_allow_html=True)
