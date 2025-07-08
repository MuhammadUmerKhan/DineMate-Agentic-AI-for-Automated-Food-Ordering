"""
# DineMate Order Management 📦

This module provides functions for managing orders in the DineMate UI.

Dependencies:
- streamlit: For UI rendering 📺.
- json: For JSON handling 🗃️.
- pandas: For data display 📊.
- re: For parsing user input 🔍.
- db_handler: For order handling logic 🛠️.
- db: For database operations 🗄️.
- logger: For structured logging 📜.
"""

import streamlit as st, json
import pandas as pd, re, time
from typing import Dict, List, Optional
from scripts.db_handler import OrderHandler
from scripts.db import Database
from scripts.logger import get_logger
from scripts.config import STATIC_CSS_PATH

logger = get_logger(__name__)
order_handler = OrderHandler()

# ✅ Load centralized CSS
try:
    with open(STATIC_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

def get_all_orders() -> List[Dict]:
    try:
        db = Database()
        query = """
        SELECT id, items, total_price, status, time, date 
        FROM orders 
        ORDER BY date DESC, time DESC
        """
        db.cursor.execute(query)
        orders = [
            {"id": row["id"], "items": row["items"], "total_price": row["total_price"],
             "status": row["status"], "time": row["time"], "date": row["date"]}
            for row in db.cursor.fetchall()
        ]
        logger.info({"message": "Fetched orders", "count": len(orders)})
        return orders
    except Exception as e:
        logger.error({"error": str(e), "message": "Failed to fetch orders"})
        st.error(f"⚠ Database error: {e}")
        return []
    finally:
        db.close_connection()

def update_order_item(order_id: str, new_items: str) -> None:
    logger.info({"order_id": order_id, "new_items": new_items, "message": "Updating order items"})
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            raise ValueError("Order ID must be a positive integer")
    except ValueError as e:
        logger.error({"error": str(e), "order_id": order_id})
        st.error(f"⚠ Invalid order ID: {e}")
        return

    try:
        new_items_dict = json.loads(new_items)
        if not isinstance(new_items_dict, dict):
            raise ValueError("Items must be a dictionary")
    except json.JSONDecodeError as e:
        logger.error({"error": str(e), "new_items": new_items})
        st.error("⚠ Invalid JSON format. Use {'item_name': quantity} format.")
        return

    valid_items = {}
    warnings = []
    total_price = 0.0
    menu = order_handler.menu

    for item, quantity in new_items_dict.items():
        item_lower = item.lower()
        if not isinstance(quantity, int) or quantity < 0:
            warnings.append(f"⚠ Invalid quantity for {item}: {quantity}")
            continue
        if item_lower in menu:
            valid_items[item_lower] = quantity
            total_price += menu[item_lower] * quantity
        else:
            warnings.append(f"⚠ {item} is not available.")

    if warnings:
        for warning in warnings:
            st.warning(warning)
        if not valid_items:
            logger.warning({"message": "No valid items", "order_id": order_id})
            return

    db = Database()
    try:
        response = db.modify_order_after_confirmation(order_id_int, valid_items, total_price)
        if "successfully" in response:
            st.success(f"✅ {response}")
            logger.info({"order_id": order_id_int, "items": valid_items, "total_price": total_price, "message": "Order updated"})
        else:
            st.error(f"⚠ {response}")
            logger.error({"order_id": order_id_int, "error": response})
    except Exception as e:
        logger.error({"error": str(e), "order_id": order_id_int})
        st.error(f"⚠ Error updating order: {e}")
    finally:
        db.close_connection()

def update_order_status(order_id: str, new_status: str) -> None:
    logger.info({"order_id": order_id, "new_status": new_status, "message": "Updating order status"})
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            raise ValueError("Order ID must be a positive integer")

        valid_statuses = ["Pending", "In Process", "Preparing", "Ready", "Completed", "Canceled", "Delivered"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}")

        db = Database()
        db.cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id_int))
        db.connection.commit()
        st.success(f"✅ Order {order_id_int} updated to {new_status}! 🎉")
        logger.info({"order_id": order_id_int, "new_status": new_status, "message": "Status updated"})
    except (ValueError, Exception) as e:
        logger.error({"error": str(e), "order_id": order_id, "new_status": new_status})
        st.error(f"⚠ Error updating status: {e}")
    finally:
        db.close_connection()

def cancel_order(order_id: str) -> None:
    logger.info({"order_id": order_id, "message": "Canceling order"})
    try:
        order_id_int = int(order_id)
        if order_id_int <= 0:
            raise ValueError("Order ID must be a positive integer")

        db = Database()
        response = db.cancel_order_after_confirmation(order_id_int)
        if "successfully" in response:
            st.success(f"✅ {response}")
            logger.info({"order_id": order_id_int, "message": "Order canceled"})
        else:
            st.warning(f"⚠ {response}")
            logger.warning({"order_id": order_id_int, "message": response})
    except ValueError as e:
        logger.error({"error": str(e), "order_id": order_id})
        st.error(f"⚠ Invalid order ID: {e}")
    except Exception as e:
        logger.error({"error": str(e), "order_id": order_id})
        st.error(f"⚠ Error canceling order: {e}")
    finally:
        db.close_connection()

def add_new_order(items_input: str) -> None:
    logger.info({"items_input": items_input, "message": "Adding new order"})
    try:
        extracted_items = extract_items_quantity(items_input)
        if not extracted_items:
            st.warning("⚠ No valid items. Use format: '2 burgers, 3 cokes'.")
            logger.warning({"items_input": items_input, "message": "No valid items"})
            return

        db = Database()
        try:
            new_order_id = db.get_max_id()
            if new_order_id is None:
                raise ValueError("Failed to generate order ID")
            total_price = sum(order_handler.menu[item] * qty for item, qty in extracted_items.items() if item in order_handler.menu)
            order_id = db.store_order_db(extracted_items, total_price)
            if order_id:
                st.success(f"✅ Order {order_id} added successfully! 🎉")
                logger.info({"order_id": order_id, "items": extracted_items, "total_price": total_price, "message": "Order added"})
            else:
                st.error("⚠ Failed to add order.")
                logger.error({"items_input": items_input, "message": "Failed to store order"})
        finally:
            db.close_connection()
    except Exception as e:
        logger.error({"error": str(e), "items_input": items_input})
        st.error(f"⚠ Error adding order: {e}")

def extract_items_quantity(user_input: str) -> Optional[Dict[str, int]]:
    logger.info({"user_input": user_input, "message": "Extracting items"})
    try:
        pattern = r'(\d+)\s+([a-zA-Z\s-]+)'
        matches = re.finditer(pattern, user_input)
        order_dict = {}
        for match in matches:
            quantity, item = match.groups()
            item = item.strip().lower()
            quantity = int(quantity)
            if quantity > 0:
                order_dict[item] = order_dict.get(item, 0) + quantity
        logger.info({"extracted_items": order_dict})
        return order_dict if order_dict else None
    except Exception as e:
        logger.error({"error": str(e), "user_input": user_input})
        return None

def show_order_management() -> None:
    logger.info({"message": "Rendering order management UI"})

    st.markdown(
        "<div class='header'><h1>📦 Order Management</h1><p style='color: #E8ECEF;'>🔄 Modify or cancel customer orders</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    with st.spinner("⏳ Loading orders..."):
        orders = get_all_orders()
    if not orders:
        st.info("✅ No orders found.")
        logger.info({"message": "No orders found"})
        return

    st.markdown("### 📝 Orders Overview")
    df = pd.DataFrame(orders)
    df.rename(columns={"id": "📦 Order ID", "items": "🍲 Items", "total_price": "💰 Total ($)",
                       "status": "🟢 Status", "time": "🕒 Time", "date": "🗓️ Date"}, inplace=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 🔍 Select Order to Modify")
    selected_order = st.selectbox("📌 Order ID", [order["id"] for order in orders], help="Choose an order to modify")

    st.divider()
    st.markdown("### ✏️ Modify Order Items")
    new_items = st.text_area("📝 Items (e.g., '2 burgers, 3 cokes')", height=68, key="modify_items", placeholder="Enter items and quantities")
    if st.button("✔ Update Items", use_container_width=True):
        with st.spinner("⏳ Updating order..."):
            extracted_items = extract_items_quantity(new_items)
            if extracted_items:
                update_order_item(selected_order, json.dumps(extracted_items))
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("⚠ Invalid items format.")
                logger.warning({"new_items": new_items, "message": "Invalid items input"})

    st.divider()
    st.markdown("### 🔄 Update Order Status")
    status_mapping = {
        "⚪ Pending": "Pending",
        "🔵 In Process": "In Process",
        "🟡 Preparing": "Preparing",
        "🟢 Ready": "Ready",
        "✅ Completed": "Completed",
        "❌ Canceled": "Canceled",
        "🚚 Delivered": "Delivered"
    }
    new_display_status = st.selectbox("🔄 New Status", list(status_mapping.keys()), key="update_status", help="Select new status")
    if st.button("✅ Update Status", use_container_width=True):
        with st.spinner("⏳ Updating status..."):
            update_order_status(selected_order, status_mapping[new_display_status])
            time.sleep(0.5)
            st.rerun()

    st.divider()
    st.markdown("### ➕ Add New Order")
    new_order_items = st.text_input("📝 New Order (e.g., '2 burgers, 3 cokes')", placeholder="Enter new order")
    if st.button("➕ Add Order", use_container_width=True):
        with st.spinner("⏳ Adding order..."):
            add_new_order(new_order_items)
            time.sleep(0.5)
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center;'>📞 Support is here for you! 🤝</p>", unsafe_allow_html=True)