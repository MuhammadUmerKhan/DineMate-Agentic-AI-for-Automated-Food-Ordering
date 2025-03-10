import streamlit as st
import json
import sqlite3
import pandas as pd
import time
from order.order_handler_lite import OrderHandler
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

# ✅ Streamlit UI for Order Management
def show_order_management():
    """✅ Customer Support Panel to manage orders (Modify, Cancel, Update Status)."""
    st.markdown("<h1 style='text-align: center;'>📦 Order Management - Customer Support</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>🔄 Modify, cancel, or update customer orders efficiently.</p>", unsafe_allow_html=True)
    st.divider()

    orders = get_all_orders()
    
    if not orders:
        st.info("✅ No orders found.")
    else:
        # ✅ Show orders in a table
        st.write("### 📝 **Customer Orders Overview**")

        # ✅ Create DataFrame & Rename Columns
        df = pd.DataFrame(orders)
        df.rename(columns={
            "id": "📦 Order ID",
            "items": "🍲 Ordered Items",
            "total_price": "💰 Total Price ($)",
            "status": "🟢 Order Status",
            "time": "🕰️ Order Time",
            "date": "🗓️ Date"
        }, inplace=True)

        # ✅ Display Orders Table
        st.dataframe(df, use_container_width=True)
        st.divider()
        
        # ✅ Select an order
        st.markdown("### ✏️ **Modify or Cancel Order**")
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            selected_order = st.selectbox("📌 Select an Order ID", [order["id"] for order in orders])
            if st.button("✔ Update Items", use_container_width=True):
                update_order_item(selected_order, new_items)
                time.sleep(1.2)
                st.rerun()

        with col2:
            new_items = st.text_area("📝 Modify Items (JSON Format)", height=68, key="modify_items")
        
        st.divider()

        # ✅ Order Status Update Section
        st.markdown("### 🔄 **Update Order Status**")
        col5, col6 = st.columns([2, 2], gap="small")

        with col5:
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
    st.markdown("<p style='text-align: center;'>📞 Need help? Customer support is here for you! 🤝</p>", unsafe_allow_html=True)
