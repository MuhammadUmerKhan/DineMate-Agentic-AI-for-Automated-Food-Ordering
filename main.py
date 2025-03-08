import streamlit as st  # Streamlit for UI
import utils  # Utility functions for chatbot and session handling
from streaming import StreamHandler  # Handles real-time streaming responses
from bot.agent import stream_graph_updates  # Function to process chatbot responses
from app import kitchen  # Import Kitchen page
from app import update_prices  # Import Admin page for updating item prices
from app import login  # ✅ Import authentication system
from app import order_management  # Import Order Management page
from app import home  # Import Home page
from app import add_remove_items # Import Add Items
from app import track_order # Import Track Order

# ✅ Set up Streamlit UI
st.set_page_config(page_title="DineMate - Food Ordering Bot", page_icon="🍽️", layout="wide")

# ✅ Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None

# ✅ Show login/register page if not authenticated
if not st.session_state["authenticated"]:
    login.login()
    st.stop()  # 🚫 Prevent unauthorized users from proceeding

# ✅ Define Role-Based Page Access (Each role gets only their assigned pages)
ROLE_PAGES = {
    "admin": ["🏠 Home", "🛡️ Update Prices", "👨‍🍳 Kitchen Orders"],  # ✅ Admin: Update Prices & Kitchen Orders
    "kitchen_staff": ["🏠 Home", "👨‍🍳 Kitchen Orders"],  # ✅ Kitchen Staff: Only Kitchen Orders
    "customer_support": ["🏠 Home", "📦 Order Management"],  # ✅ Support: Manage Orders
    "customer": ["🏠 Home", "🍔 DineMate Chatbot", "📦 Track Order"]  # ✅ Customers: Order, Chat, & Track Orders
}

# ✅ Sidebar Title & Welcome Message
st.sidebar.title("📌 Navigation")
st.sidebar.markdown(f"👋 **Welcome, {st.session_state['username']}!**")

# ✅ Get allowed pages for the logged-in role
available_pages = ROLE_PAGES.get(st.session_state["role"], [])

# ✅ If the user has no assigned pages, show warning
if not available_pages:
    st.warning("⚠ You do not have access to any pages.")
    st.stop()

# ✅ Sidebar navigation
page = st.sidebar.radio("📌 Select Page", available_pages)

# 🎯 Load Selected Page
if page == "🏠 Home":
    home.home()

elif page == "🍔 DineMate Chatbot":
    st.title("🍽️ DineMate - AI Food Ordering Chatbot")

    # ✅ Display GitHub Source Code Button
    st.write('[![View Source Code](https://img.shields.io/badge/view_source_code-gray?logo=github)]'
             '(https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot)')

    # ✅ Enable Chat History
    @utils.enable_chat_history
    def chatbot_main():
        """Main function to handle chatbot interactions."""
        user_query = st.chat_input(placeholder="Ask me anything about food ordering!")

        if user_query:
            utils.display_msg(user_query, "user")  

            with st.chat_message("assistant"):  
                st_sb = StreamHandler(st.empty())  

                try:
                    response = stream_graph_updates(user_query)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    utils.print_qa(chatbot_main, user_query, response)

                except Exception as e:
                    error_msg = f"⚠ Error processing request: {str(e)}"
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    chatbot_main()  # ✅ Run chatbot

elif page == "👨‍🍳 Kitchen Orders":
    kitchen.show_kitchen_orders()

elif page == "🛡️ Update Prices":
    update_prices.show_price_update_page()

elif page == "📦 Order Management":
    order_management.show_order_management()
elif page == "➕ Add/Remove Items":
    add_remove_items.show_add_remove_items_page()  
elif page == "📦 Track Order":
    track_order.show_order_tracking()
  
# ✅ Add Logout Button in Sidebar
if st.sidebar.button("🚪 Logout"):
    login.logout()
