import streamlit as st
import mysql.connector
import pandas as pd  # ✅ Import Pandas for DataFrame
import time
from config import DB_CONFIG  # ✅ Database connection configuration

def get_menu_items():
    """✅ Fetch all menu items with their current prices."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT name, price FROM menu"
        cursor.execute(query)
        items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return items
    
    except Exception as e:
        st.error(f"⚠ Database error: {e}")
        return []

def update_item_price(item_name, new_price):
    """✅ Update the price of a selected item."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = "UPDATE menu SET price = %s WHERE name = %s"
        cursor.execute(query, (new_price, item_name))
        conn.commit()
        
        cursor.close()
        conn.close()
        st.success(f"✅ Price for **{item_name}** updated to **${new_price:.2f}**!")

    except Exception as e:
        st.error(f"⚠ Error updating price: {e}")

# ✅ Streamlit UI for Authorized Users
def show_price_update_page():
    """✅ Page for updating item prices."""
    st.title("🔑 Admin Panel - Update Item Prices")
    st.write("### View & Update Menu Prices")

    menu_items = get_menu_items()

    if not menu_items:
        st.info("✅ No menu items found.")
    else:
        # ✅ Display menu items in a DataFrame
        st.write("### 📋 Current Menu & Prices")

        # ✅ Convert to DataFrame and format prices
        df_menu = pd.DataFrame(menu_items)
        df_menu["price"] = df_menu["price"].astype(float)  # ✅ Convert Decimal to float for display
        df_menu.rename(columns={"name": "🍲 Item Name", "price": "Price ($)"}, inplace=True)

        # # ✅ Show table with full width
        # st.dataframe(df_menu, use_container_width=True, height=400)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ✅ Select an item to update
            item_dict = {item["name"]: float(item["price"]) for item in menu_items}  # ✅ Convert Decimal to float
            selected_item = st.selectbox("Select Item to Update:", list(item_dict.keys()))
            current_price = item_dict[selected_item]
        with col2:
            # ✅ Input new price
            new_price = st.number_input("Enter New Price ($)", min_value=0.01, value=current_price, step=0.01, format="%.2f")

        # ✅ Update Price Button
        if st.button("✔ Update Price"):
            update_item_price(selected_item, new_price)
            time.sleep(1.2)  # ⏳ Delay for 2 seconds
            st.rerun()  # Refresh the page after update
        
        # ✅ Show table with full width
        st.dataframe(df_menu, use_container_width=True, width=400)
