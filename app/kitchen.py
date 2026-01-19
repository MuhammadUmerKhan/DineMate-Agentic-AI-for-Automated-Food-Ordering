"""
# DineMate Kitchen Dashboard 👨‍🍳

This module provides the kitchen staff interface for managing orders.

Dependencies:
- streamlit: For UI rendering 📺.
- pandas: For data display 📊.
- db: For database operations 🗄️.
- logger: For structured logging 📜.
"""

import streamlit as st, time
import pandas as pd
from datetime import datetime
from scripts.db import Database
from scripts.logger import get_logger
from scripts.config import STATIC_CSS_PATH
from typing import List, Dict
from streamlit_autorefresh import st_autorefresh

logger = get_logger(__name__)

# ✅ Load centralized CSS
try:
    with open(STATIC_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

def get_kitchen_orders(status: str = "Pending") -> List[Dict]:
    try:
        db = Database()
        query = "SELECT id, items, total_price, status, time, date FROM orders WHERE status = ?"
        db.cursor.execute(query, (status,))
        orders = [
            {"id": row["id"], "items": row["items"], "total_price": row["total_price"],
             "status": row["status"], "time": row["time"], "date": row["date"]}
            for row in db.cursor.fetchall()
        ]
        logger.info({"status": status, "count": len(orders), "message": "Fetched kitchen orders"})
        return orders
    except Exception as e:
        logger.error({"error": str(e), "status": status, "message": "Failed to fetch kitchen orders"})
        st.error(f"⚠ Database error: {e}")
        return []
    finally:
        db.close_connection()

def update_order_status(order_id: int, new_status: str) -> None:
    logger.info({"order_id": order_id, "new_status": new_status, "message": "Updating order status"})
    try:
        db = Database()
        db.cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        db.connection.commit()
        st.success(f"✅ Order {order_id} updated to {new_status}! 🎉")
        logger.info({"order_id": order_id, "new_status": new_status, "message": "Status updated"})
    except Exception as e:
        logger.error({"error": str(e), "order_id": order_id, "new_status": new_status})
        st.error(f"⚠ Error updating order: {e}")
    finally:
        db.close_connection()

def show_kitchen_orders() -> None:
    st_autorefresh(interval=10_000, key="kitchen_refresh")

    st.markdown(
        "<div class='header'><h1>👨‍🍳 Kitchen Orders</h1><p style='color: #E8ECEF;'>🍳 Manage and update order statuses</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    status_mapping = {
        "⚪ Pending": "Pending",
        "🔵 In Process": "In Process",
        "🟡 Preparing": "Preparing",
        "🟢 Ready": "Ready",
        "✅ Completed": "Completed",
        "❌ Canceled": "Canceled",
        "🚚 Delivered": "Delivered"
    }

    selected_display_status = st.selectbox(
        "🔍 Filter Orders by Status", list(status_mapping.keys()), help="Choose order status to view"
    )
    selected_status = status_mapping[selected_display_status]

    with st.spinner("⏳ Loading orders..."):
        orders = get_kitchen_orders(selected_status)

    if not orders:
        st.info(f"✅ No {selected_status} orders.")
        logger.info({"status": selected_status, "message": "No orders found"})
    else:
        st.markdown("### 📝 Orders List")
        df = pd.DataFrame(orders)
        df["time"] = df["time"].apply(lambda x: datetime.strptime(x, "%I:%M:%S %p").strftime("%I:%M %p"))
        df.rename(columns={
            "id": "📦 Order ID", "items": "🍲 Ordered Items", "total_price": "💰 Total Price ($)",
            "status": "🟢 Current Status", "time": "🕒 Order Time", "date": "🗓️ Date"
        }, inplace=True)
        st.dataframe(df, width="stretch", hide_index=True)

        if st.session_state.get("role") == "kitchen_staff":
            st.markdown("### 🔄 Update Order Status")
            col1, col2 = st.columns(2)
            with col1:
                selected_order = st.selectbox("📌 Select Order", [order["id"] for order in orders], help="Choose an order to update")
            with col2:
                new_display_status = st.selectbox("🚀 New Status", list(status_mapping.keys()), help="Select new status")
                new_status = status_mapping[new_display_status]

            if st.button("✔ Update Status", width="stretch"):
                with st.spinner("⏳ Updating status..."):
                    update_order_status(selected_order, new_status)
                    time.sleep(0.5)
                    st.rerun()
        else:
            st.markdown(
                "<div class='warning-container'><h3 style='color: #EF0606;'>⚠ Access Denied</h3><p>Only kitchen staff can update order status.</p></div>",
                unsafe_allow_html=True
            )