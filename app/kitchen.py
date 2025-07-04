import streamlit as st
import sqlite3
import pandas as pd
import time  # ⏳ Import time module for delay
from scripts.config import DB_PATH
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ✅ Establish database connection
def get_connection():
    """🔌 Establish connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

# ✅ Fetch Kitchen Orders based on status
def get_kitchen_orders(status="Pending"):
    # ✅ Auto-refresh every 10 seconds
    st_autorefresh(interval=10 * 1000, key="kitchen_refresh")  # 🔄 Refresh every 10 seconds
    """📦 Fetch orders placed more than 10 minutes ago, considering both date & time correctly."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ✅ Fetch all orders with the given status
        query = "SELECT id, items, total_price, status, time, date FROM orders WHERE status = ?"
        cursor.execute(query, (status,))
        orders = cursor.fetchall()
        conn.close()

        # ✅ Get current time
        now = datetime.now()

        # ✅ Filter orders older than 10 minutes
        valid_orders = []
        for row in orders:
            order_id, items, total_price, order_status, time_str, date_str = row

            # ✅ Convert stored date & time (which are strings) into datetime format
            try:
                order_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M:%S %p")
            except ValueError as e:
                st.error(f"⚠ Invalid date/time format for Order ID {order_id}: {date_str} {time_str} - {e}")
                continue  # Skip this order if the format is incorrect

            # ✅ Check if the order was placed more than 10 minutes ago
            if order_datetime <= now - timedelta(minutes=10):
                valid_orders.append({
                    "id": order_id,
                    "items": items,
                    "total_price": total_price,
                    "status": order_status,
                    "time": order_datetime.strftime("%I:%M %p"),  # ✅ Convert back to readable format
                    "date": date_str
                })

        return valid_orders

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

    # ✅ Mapping of statuses (UI display with emoji → Database values)
    status_mapping = {
        "⚪ Pending": "Pending",
        "🔵 In Process": "In Process",
        "🟡 Preparing": "Preparing",
        "🟢 Ready": "Ready",
        "✅ Completed": "Completed",
        "❌ Canceled": "Canceled",
        "🚚 Delivered": "Delivered"
    }
    
    # ✅ Show selectbox with emoji options
    selected_display_status = st.selectbox("🔍 **Filter Orders by Status**:", list(status_mapping.keys()))

    # ✅ Convert the selected display value to the actual database status
    selected_status = status_mapping[selected_display_status]

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
            order["time"] = datetime.strptime(order["time"], "%I:%M %p").strftime("%I:%M %p")

        order_data = pd.DataFrame(orders)
        order_data.rename(columns={
            "id": "📦 Order ID",
            "items": "🍲 Ordered Items",
            "total_price": "💰 Total Price ($)",
            "status": "🟢 Current Status",
            "time": "🕒 Order Time",
            "date": "🗓️ Date"
        }, inplace=True)

        # ✅ Show Orders in an Interactive Table
        st.dataframe(order_data, use_container_width=True, hide_index=True) 

        # ✅ Kitchen Staff - Order Status Update
        if st.session_state.get("role") == "kitchen_staff":
            st.markdown("### 🔄 **Update Order Status**")
            col1, col2 = st.columns(2)

            with col1:
                selected_order = st.selectbox("📌 Select Order to Update:", [order["id"] for order in orders])

            # ✅ Mapping for UI display (emoji) and database values
            status_mapping = {
                "⚪ Pending": "Pending",
                "🔵 In Process": "In Process",
                "🟡 Preparing": "Preparing",
                "🟢 Ready": "Ready",
                "✅ Completed": "Completed",
                "❌ Canceled": "Canceled",
                "🚚 Delivered": "Delivered"
            }
            with col2:
                # ✅ Show selectbox with emoji options
                new_display_status = st.selectbox("🚀 **Select New Status:**", list(status_mapping.keys()))

                # ✅ Convert selected emoji status to database-friendly value
                new_status = status_mapping[new_display_status]

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
