import streamlit as st
import sqlite3
import pandas as pd
import time  # ⏳ Import time module for delay
from config import DB_PATH
from datetime import datetime

# ✅ Establish database connection
def get_connection():
    """🔌 Establish connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

# ✅ Fetch Kitchen Orders based on status
def get_kitchen_orders(status="Pending"):
    """📦 Fetch only orders that were placed more than 10 minutes ago and match the selected status."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, items, total_price, status, time 
        FROM orders
        WHERE status = ?
        AND datetime(date || ' ' || time) <= datetime('now', '-10 minutes')
        """
        cursor.execute(query, (status,))
        orders = [{"id": row[0], "items": row[1], "total_price": row[2], "status": row[3], "time": row[4]} for row in cursor.fetchall()]
        
        conn.close()
        return orders
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

# ✅ Update Order Status (Restricted to Kitchen Staff)
def update_order_status(order_id, new_status):
    """🔄 Update the status of an order (Only for Kitchen Staff)."""
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

# ✅ Streamlit UI for Kitchen Staff
def show_kitchen_orders():
    """👨‍🍳 Kitchen Staff Dashboard - Manage Orders"""
    
    # ✅ Title with Emoji
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>👨‍🍳 Kitchen Staff Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>📦 View & Manage Active Orders</h3>", unsafe_allow_html=True)
    st.divider()

    # ✅ Status Filter for Kitchen Orders
    selected_status = st.selectbox("🔍 **Filter Orders by Status**:", ["Pending", "In Process", "Preparing", "Ready", "Delivered"])
    
    # ✅ Fetch Orders (Older than 10 minutes with selected status)
    orders = get_kitchen_orders(selected_status)
    
    if not orders:
        st.info(f"✅ No **{selected_status}** orders.")
    else:
        # ✅ Display Orders in a Styled Table
        st.markdown("### 📝 **Orders List**")

        # ✅ Convert Orders to DataFrame
        for order in orders:
            # Convert order time from 24-hour format to 12-hour format (e.g., "14:30:00" → "02:30 PM")
            order["time"] = datetime.strptime(order["time"], "%H:%M:%S").strftime("%I:%M %p")

        order_data = pd.DataFrame(orders)
        order_data.rename(columns={
            "id": "📦 Order ID",
            "items": "🍲 Ordered Items",
            "total_price": "💰 Total Price ($)",
            "status": "🟢 Current Status",
            "time": "🕒 Order Time"
        }, inplace=True)

        # ✅ Show Orders in an Interactive Table
        st.dataframe(order_data, use_container_width=True, hide_index=True) 

        # ✅ Kitchen Staff - Order Status Update
        if st.session_state.get("role") == "kitchen_staff":
            st.markdown("### 🔄 **Update Order Status**")
            col1, col2 = st.columns(2)

            with col1:
                selected_order = st.selectbox("📌 Select Order to Update:", [order["id"] for order in orders])

            with col2:
                # ✅ Limit status updates to valid options
                new_status = st.selectbox("🚀 Select New Status:", ["Pending", "In Process", "Preparing", "Ready", "Completed", "Delivered"])

            # ✅ Button with Animation
            col3, col4, col5 = st.columns([1, 2, 1])
            with col4:
                if st.button("✔ Update Order Status", use_container_width=True):
                    update_order_status(selected_order, new_status)
                    time.sleep(1.2)  # ⏳ Delay for animation
                    st.rerun()  # 🔄 Refresh page after update
        else:
            st.warning("⚠ You do not have permission to update order status.", icon="🚫")  # ❌ Restrict Admin

# ✅ Run the Kitchen Orders Page
if __name__ == "__main__":
    show_kitchen_orders()
