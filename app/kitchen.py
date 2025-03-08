import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import time
from config import DB_CONFIG  # ✅ Database connection configuration

def get_kitchen_orders():
    """✅ Fetch only orders that were placed more than 10 minutes ago."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # ✅ Combine `date` and `time` into a full DATETIME column for accurate filtering
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

def update_order_status(order_id, new_status):
    """✅ Update the status of an order (Only for Kitchen Staff)."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = "UPDATE orders SET status = %s WHERE id = %s"
        cursor.execute(query, (new_status, order_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        st.success(f"✅ Order {order_id} updated to **{new_status}**!")

    except Exception as e:
        st.error(f"⚠ Error updating order: {e}")

# ✅ Streamlit UI for Kitchen Staff
def show_kitchen_orders():
    """✅ Display orders that cannot be canceled in a table format."""
    st.title("👨‍🍳 Kitchen Staff Dashboard")
    st.write("### Orders that cannot be canceled (Past 10-Minute Window)")

    orders = get_kitchen_orders()
    
    if not orders:
        st.info("✅ No active orders older than 10 minutes.")
    else:
        st.write("### 📝 Orders List")

        # ✅ Create DataFrame-style table layout
        order_data = pd.DataFrame(orders, columns=["id", "items", "total_price", "status"])
        order_data.rename(columns={
            "id": "📦 Order ID",
            "items": "🍲 Ordered Items",
            "total_price": "$ Total Price",
            "status": "🟢 Current Status"
        }, inplace=True)

        # ✅ Show the table with proper headers
        st.dataframe(order_data, use_container_width=True)  # ✅ Full-width, better size

        # ✅ Restrict Access: Only allow Kitchen Staff to update order status
        if st.session_state["role"] == "kitchen_staff":
            st.write("### 🔄 Update Order Status")
            col1, col2 = st.columns(2)  # ✅ Create two columns

            with col1:
                selected_order = st.selectbox("Select Order to Update:", [order["id"] for order in orders])

            with col2:
                new_status = st.selectbox("Select New Status:", ["Pending", "In Process", "Preparing", "Ready", "Completed"])

            if st.button("✔ Update Order Status"):
                update_order_status(selected_order, new_status)
                time.sleep(1.2)  # ⏳ Delay for 2 seconds
                st.rerun()  # Refresh page after update
        else:
            st.warning("⚠ You do not have permission to update order status.")  # ❌ Admin Restricted
