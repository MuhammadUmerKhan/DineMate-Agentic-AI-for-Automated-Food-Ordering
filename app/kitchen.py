import streamlit as st
import mysql.connector
from datetime import datetime, timedelta
from config import DB_CONFIG  # ✅ Database connection configuration

def get_kitchen_orders():
    """✅ Fetch non-cancelable orders (older than 10 minutes) from the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Get current time and calculate cutoff time (10 minutes)
        cutoff_time = datetime.now() - timedelta(minutes=10)
        
        query = """
        SELECT * FROM orders
        WHERE status = 'Pending'
        AND time <= %s
        """
        cursor.execute(query, (cutoff_time,))
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return orders
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

def update_order_status(order_id, new_status):
    """✅ Update the status of an order."""
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
        st.info("✅ No active orders at the moment.")
    else:
        st.write("### 📝 Orders List")
        order_ids = []
        statuses = []

        # ✅ Create table layout
        table_data = []
        for order in orders:
            order_ids.append(order["id"])
            statuses.append(order["status"])
            table_data.append([
                f"📦 Order #{order['id']}",
                order["items"],
                f"${order['total_price']:.2f}",
                order["status"]
            ])

        # ✅ Show orders in a table format
        st.table(table_data)

        # ✅ Update Order Status
        st.write("### 🔄 Update Order Status")

        selected_order = st.selectbox("Select Order to Update:", order_ids)
        new_status = st.selectbox("Select New Status:", ["Pending", "In Process", "Preparing", "Ready", "Completed"])

        if st.button("✔ Update Order Status"):
            update_order_status(selected_order, new_status)
            st.experimental_rerun()  # Refresh page after update
