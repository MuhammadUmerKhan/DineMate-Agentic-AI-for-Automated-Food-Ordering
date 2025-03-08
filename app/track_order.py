import streamlit as st
import mysql.connector
from config import DB_CONFIG

def get_order_details(order_id):
    """✅ Fetch order details from the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()

        cursor.close()
        conn.close()
        return order
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return None

def show_order_tracking():
    """✅ Customer Order Tracking Page."""
    st.title("📦 Track Your Order")
    st.write("### Enter your **Order ID** below to check your order status.")

    order_id = st.text_input("🔍 Enter Order ID")

    if st.button("🚀 Track Order"):
        if not order_id.strip().isdigit():
            st.warning("⚠ Please enter a **valid numeric Order ID**.")
            return

        order = get_order_details(order_id)

        if order:
            st.success("✅ Order Found! Here are your order details:")
            st.write("### 📝 **Order Summary**")
            st.write(f"📦 **Order ID:** {order['id']}")
            st.write(f"🛒 **Items Ordered:** {order['items']}")
            st.write(f"💰 **Total Price:** ${order['total_price']:.2f}")
            st.write(f"📌 **Current Status:** {order['status']}")
            
            # if order["status"] not in ["Canceled", "Completed"]:
                # st.write(f"⏳ **Estimated Delivery Time:** {order['time']}")

        else:
            st.error("⚠ No order found with this **Order ID**. Please check and try again.")