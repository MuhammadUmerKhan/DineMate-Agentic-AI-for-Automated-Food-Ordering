import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import time
from config import DB_CONFIG  # ✅ Database connection configuration

# ✅ Fetch Kitchen Orders (Older than 10 min)
def get_kitchen_orders():
    """📦 Fetch only orders that were placed more than 10 minutes ago."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # ✅ Fetch orders that cannot be canceled
        query = """
        SELECT id, items, total_price, status
        FROM orders
        WHERE status = 'Pending'
        AND STR_TO_DATE(CONCAT(date, ' ', time), '%Y-%m-%d %H:%i:%s') <= NOW() - INTERVAL 10 MINUTE
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return orders
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

# ✅ Update Order Status (Restricted to Kitchen Staff)
def update_order_status(order_id, new_status):
    """🔄 Update the status of an order (Only for Kitchen Staff)."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = "UPDATE orders SET status = %s WHERE id = %s"
        cursor.execute(query, (new_status, order_id))
        conn.commit()
        
        cursor.close()
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

    # ✅ Fetch Orders (Older than 10 minutes)
    orders = get_kitchen_orders()
    
    if not orders:
        st.info("✅ No active orders older than **10 minutes**.")
    else:
        # ✅ Display Orders in a Styled Table
        st.markdown("### 📝 **Orders List**")

        # ✅ Convert Orders to DataFrame
        order_data = pd.DataFrame(orders, columns=["id", "items", "total_price", "status"])
        order_data.rename(columns={
            "id": "📦 Order ID",
            "items": "🍲 Ordered Items",
            "total_price": "💰 Total Price ($)",
            "status": "🟢 Current Status"
        }, inplace=True)

        # ✅ Show Orders in an Interactive Table
        st.dataframe(order_data, use_container_width=True, hide_index=True) 

        # ✅ Kitchen Staff - Order Status Update
        if st.session_state["role"] == "kitchen_staff":
            st.markdown("### 🔄 **Update Order Status**")
            col1, col2 = st.columns(2)

            with col1:
                selected_order = st.selectbox("📌 Select Order to Update:", [order["id"] for order in orders])

            with col2:
                # ✅ Limit status updates to valid options
                new_status = st.selectbox("🚀 Select New Status:", ["Pending", "In Process", "Preparing", "Ready", "Completed"])

            # ✅ Button with Animation
            col3, col4, col5 = st.columns([1, 2, 1])
            with col4:
                if st.button("✔ Update Order Status", use_container_width=True):
                    update_order_status(selected_order, new_status)
                    time.sleep(1.2)  # ⏳ Delay for animation
                    st.rerun()  # 🔄 Refresh page after update

        else:
            st.warning("⚠ You do not have permission to update order status.", icon="🚫")  # ❌ Restrict Admin
