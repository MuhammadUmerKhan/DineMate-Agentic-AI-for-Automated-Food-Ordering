import streamlit as st
import json
import mysql.connector
from order.order_handler import OrderHandler
from config import DB_CONFIG
import time
import pandas as pd

# ✅ Initialize the order handler
order_handler = OrderHandler()

def get_all_orders():
    """✅ Fetch all customer orders from the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, items, total_price, status, time FROM orders"
        cursor.execute(query)
        orders = cursor.fetchall()

        cursor.close()
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
    response = order_handler.db.update_order_status(order_id, new_status)
    
    if "✅" in response:
        st.success(response)
    else:
        st.warning(response)

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
    st.title("📦 Order Management - Customer Support")
    st.write("### View, Modify, or Cancel Customer Orders")

    orders = get_all_orders()
    
    if not orders:
        st.info("✅ No orders found.")
    else:
        st.markdown("---")
        # ✅ Show orders in a table
        st.write("### 📝 Customer Orders")
        
        # ✅ Create DataFrame
        df = pd.DataFrame(orders)

        # ✅ Rename columns properly
        df.rename(columns={
            "id": "📦 ID",
            "items": "🍲 Items",
            "total_price": "$ Total Price",
            "status": "🟢 Status",
            "time": "🕰️ Time"
        }, inplace=True)
        st.dataframe(df, use_container_width=True, width=400)

        st.markdown("---")
        
        # ✅ Select an order
        order_ids = [order["id"] for order in orders]

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown("#### Select Order to Modify")  
            selected_order = st.selectbox("", order_ids, key="select_order", label_visibility="collapsed")

        with col2:
            st.markdown("#### Modify Items (Enter JSON Format)")  
            new_items = st.text_area("", height=68, key="modify_items", label_visibility="collapsed")
        
        # ✅ Buttons in the same row
        # col1 = st.columns(1)

        # with col1:
        if st.button("✔ Update Items", use_container_width=True):
            update_order_item(selected_order, new_items)
            time.sleep(1.2)  
            st.rerun()  

        st.markdown("---")
        
        # with col4:
        #     if st.button("❌ Cancel Order", use_container_width=True):
        #         cancel_order(selected_order)
        #         time.sleep(1.2)  
        #         st.rerun()  

        # with col5:
        st.markdown("#### Update Order Status")
        new_status = st.selectbox("", ["Pending", "In Process", "Preparing", "Ready", "Completed", "Canceled"], key="update_status", label_visibility="collapsed")

        if st.button("🔄 Update Status", use_container_width=True):
            update_order_status(selected_order, new_status)
            time.sleep(1.2)  
            st.rerun()  
