import streamlit as st
import sqlite3
import pandas as pd  # ✅ Import Pandas for DataFrame
import time
from config import *

def get_connection():
    """🔌 Establish connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def get_menu_items():
    """✅ Fetch all menu items with their current prices."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT name, price FROM menu"
        cursor.execute(query)
        items = cursor.fetchall()

        conn.close()
        
        return [{"name": row[0], "price": row[1]} for row in items]
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

def update_item_price(item_name, new_price):
    """✅ Update the price of a selected item."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "UPDATE menu SET price = ? WHERE name = ?"
        cursor.execute(query, (new_price, item_name))
        conn.commit()
        conn.close()

        st.success(f"✅ Price for **{item_name}** updated to **${new_price:.2f}**! 🎉")

    except Exception as e:
        st.error(f"⚠ Error updating price: {e}")

# ✅ Streamlit UI for Authorized Users
def show_price_update_page():
    """✅ Page for updating item prices."""
    st.markdown("<h1 style='text-align: center; color: #007BFF;'>🔑 Admin Panel - Update Item Prices</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>📋 View & Modify Menu Prices</h3>", unsafe_allow_html=True)
    st.divider()

    menu_items = get_menu_items()

    if not menu_items:
        st.info("✅ No menu items found.")
    else:
        # ✅ Display menu items in a DataFrame
        st.write("### 📜 **Current Menu & Prices**")
        
        # ✅ Convert to DataFrame and format prices
        df_menu = pd.DataFrame(menu_items)
        df_menu["price"] = df_menu["price"].astype(float)  # ✅ Convert Decimal to float for display
        df_menu.rename(columns={"name": "🍲 Item Name", "price": "💰 Price ($)"}, inplace=True)

        st.dataframe(df_menu, use_container_width=True, width=500)

        st.markdown("---")

        # ✅ Layout for Updating Price
        st.write("### ✏ **Modify Item Price**")
        col1, col2 = st.columns([2, 2])

        with col1:
            # ✅ Select an item to update
            item_dict = {item["name"]: float(item["price"]) for item in menu_items}  # ✅ Convert Decimal to float
            selected_item = st.selectbox("📌 Select Item:", list(item_dict.keys()))
            current_price = item_dict[selected_item]
        
        with col2:
            # ✅ Input new price
            new_price = st.number_input("💵 Enter New Price ($)", min_value=0.01, value=current_price, step=0.01, format="%.2f")

        st.markdown("---")

        # ✅ Update Price Button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔ Update Price", use_container_width=True):
                st.info("⏳ Updating price... Please wait.")
                time.sleep(1.5)  # ⏳ Simulate processing delay
                update_item_price(selected_item, new_price)
                st.rerun()  # Refresh the page after update

        with col2:
            if st.button("🔄 Reset Selection", use_container_width=True):
                st.rerun()  # 🔄 Reset selections & refresh page
