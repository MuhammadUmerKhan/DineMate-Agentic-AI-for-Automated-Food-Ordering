"""
# DineMate Order Tracking 📦

This module allows customers to track orders.

Dependencies:
- streamlit: For UI rendering 📺.
- json: For JSON handling 🗃️.
- db: For database operations 🗄️.
- logger: For structured logging 📜.
"""

import streamlit as st, json
from scripts.db import Database
from scripts.logger import get_logger
from typing import Optional, Dict

logger = get_logger(__name__)

def get_order_details(order_id: str) -> Optional[Dict]:
    """🔍 Fetch order details from the database.

    Args:
        order_id (str): Order ID.

    Returns:
        Optional[Dict]: Order details or None if not found.
    """
    logger.info({"order_id": order_id, "message": "Fetching order details"})
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            raise ValueError("Order ID must be a positive integer")
        db = Database()
        db.cursor.execute("SELECT id, items, total_price, status FROM orders WHERE id = ?", (order_id_int,))
        row = db.cursor.fetchone()
        if row:
            order = {"id": row["id"], "items": row["items"], "total_price": row["total_price"], "status": row["status"]}
            logger.info({"order_id": order_id_int, "message": "Order details fetched"})
            return order
        logger.warning({"order_id": order_id_int, "message": "Order not found"})
        return None
    except ValueError as e:
        logger.error({"error": str(e), "order_id": order_id})
        return None
    except Exception as e:
        logger.error({"error": str(e), "order_id": order_id})
        st.error(f"⚠ Database error: {e}")
        return None
    finally:
        db.close_connection()

def show_order_tracking() -> None:
    """📦 Display the order tracking page."""
    st.markdown(
            "<div class='header'><h1>📦 Track Order</h1><p style='color: #E8ECEF;'>🚚 Check real-time order status</p></div>",
            unsafe_allow_html=True
        )
    order_id = st.text_input("🔢 Order ID", placeholder="e.g., 12345").strip()
    if st.button("🚀 Track Order", width="stretch"):
        with st.spinner("⏳ Fetching order details..."):
            if not order_id.isdigit():
                st.warning("⚠ Please enter a valid numeric Order ID.")
                logger.warning({"order_id": order_id, "message": "Invalid order ID"})
                return
            order = get_order_details(order_id)
            if order:
                st.success("✅ Order found!")
                st.markdown("### 📝 Order Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"📦 **Order ID:** {order['id']}")
                    items_dict = json.loads(order['items'])
                    items_list = "".join([f"<li><strong>{item.title()}</strong>: {quantity}</li>" for item, quantity in items_dict.items()])
                    st.markdown(f"🛒 **Items**:\n\n{items_list}", unsafe_allow_html=True)
                    st.write(f"💰 **Total Price**: ${order['total_price']:.2f}")
                status_colors = {
                    "Pending": "⚪ **Pending** - Waiting to be processed.",
                    "In Process": "🔵 **In Process** - Being prepared.",
                    "Preparing": "🟡 **Preparing** - Food is being cooked.",
                    "Ready": "🟢 **Ready** - Ready for pickup/delivery.",
                    "Completed": "✅ **Completed** - Delivered!",
                    "Canceled": "❌ **Canceled** - Order was canceled.",
                    "Delivered": "🚚 **Delivered** - Order has been delivered!"
                }
                st.markdown(f"📌 **Status**: {status_colors.get(order['status'], '🔘 Unknown Status')}")
            else:
                st.error("⚠ No order found with this ID.")
                logger.warning({"order_id": order_id, "message": "Order not found"})