"""
# DineMate Main Application 🍽️

This module sets up the Streamlit UI for the DineMate food ordering chatbot with an enhanced dark theme.

Dependencies:
- streamlit: For UI rendering 📺.
- scripts.utils: For chatbot and session handling 🛠️.
- scripts.streaming: For real-time streaming responses 🌐.
- app modules: For specific pages (home, kitchen, analysis, etc.) 📄.
- time: For UI delays ⏳.
"""

import streamlit as st, time
import scripts.utils as utils
from scripts.config import STATIC
from scripts.streaming import StreamHandler, stream_graph_updates
from app import kitchen, update_prices, login, order_management, home, add_remove_items, track_order, analysis
from scripts.logger import get_logger

logger = get_logger(__name__)

# ✅ Set up Streamlit UI with dark theme
st.set_page_config(page_title="DineMate - Food Ordering Bot", page_icon="🍽️", layout="wide")

# ✅ Load centralized CSS
try:
    with open(STATIC, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

# ✅ Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None

# ✅ Show login/register page if not authenticated
if not st.session_state["authenticated"]:
    login.login()
    st.stop()

# 🎨 Sidebar with enhanced navigation
st.sidebar.markdown(
    "<div class='header'><h2 style='color: #E8ECEF;'>🍽️ DineMate</h2><p style='color: #FFA500;'>Order Smarter with AI</p></div>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f"<h3 style='text-align: center;'>👋 <span style='color: #FFA500;'>{st.session_state['username'].title()}</span> ({st.session_state['role'].title()})</h3>",
    unsafe_allow_html=True
)

# ✅ Define Role-Based Page Access
ROLE_PAGES = {
    "admin": [
        {"label": "🏠 Home", "tooltip": "View DineMate overview"},
        {"label": "🛡️ Update Prices", "tooltip": "Manage menu prices"},
        {"label": "👨‍🍳 Kitchen Orders", "tooltip": "Handle kitchen tasks"},
        {"label": "➕ Add/Remove Items", "tooltip": "Update menu items"},
        {"label": "📶 Analysis", "tooltip": "Explore business insights"}
    ],
    "kitchen_staff": [
        {"label": "🏠 Home", "tooltip": "View DineMate overview"},
        {"label": "👨‍🍳 Kitchen Orders", "tooltip": "Handle kitchen tasks"}
    ],
    "customer_support": [
        {"label": "🏠 Home", "tooltip": "View DineMate overview"},
        {"label": "📦 Order Management", "tooltip": "Manage customer orders"}
    ],
    "customer": [
        {"label": "🏠 Home", "tooltip": "View DineMate overview"},
        {"label": "🍔 DineMate Chatbot", "tooltip": "Order with AI chatbot"},
        {"label": "🎙️ Voice Chat", "tooltip": "Order with voice"},
        {"label": "📦 Track Order", "tooltip": "Check order status"}
    ]
}

# ✅ Get allowed pages for the logged-in role
available_pages = [page["label"] for page in ROLE_PAGES.get(st.session_state["role"], [])]
tooltips = {page["label"]: page["tooltip"] for page in ROLE_PAGES.get(st.session_state["role"], [])}

# 🚨 If no assigned pages, show warning
if not available_pages:
    st.markdown(
        "<div class='warning-container'><h3 style='color: #EF0606;'>⚠ No Access</h3><p>You do not have access to any pages.</p></div>",
        unsafe_allow_html=True
    )
    st.stop()

# ✅ Sidebar Navigation Menu with tooltips
page = st.sidebar.radio(
    "� Ascending",
    available_pages,
    format_func=lambda x: x,
    label_visibility="collapsed"
)
for label in available_pages:
    st.markdown(f"<style>.stRadio label[data-label='{label}']::after {{ content: '{tooltips[label]}'; }}</style>", unsafe_allow_html=True)

# 🎯 Load Selected Page
if page == "🏠 Home":
    home.home()

elif page == "🍔 DineMate Chatbot":
    st.markdown(
        "<div class='header'><h1>🤖 DineMate Chatbot</h1><p style='color: #E8ECEF;'>🍔 Order food with our intelligent AI agent</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    @utils.enable_chat_history
    def chatbot_main():
        user_query = st.chat_input(placeholder="💬 Type your order (e.g., '2 burgers and a coke')...")

        if user_query:
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**You**: {user_query}")
                logger.info({"user": st.session_state["username"], "query": user_query, "message": "User submitted chatbot query"})

            with st.chat_message("assistant", avatar="🍔"):
                st_sb = StreamHandler(st.empty())
                try:
                    with st.spinner("🍴 Processing your order..."):
                        response = stream_graph_updates(user_query)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        utils.print_qa(chatbot_main, user_query, response)
                        logger.info({"user": st.session_state["username"], "response": response, "message": "Chatbot response generated"})
                except Exception as e:
                    error_msg = f"⚠ Error processing request: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    logger.error({"user": st.session_state["username"], "error": str(e), "message": "Chatbot error"})

    chatbot_main()

elif page == "🎙️ Voice Chat":
    st.markdown(
        "<div class='header'><h1>🎙️ Voice Chat with DineMate</h1><p style='color: #E8ECEF;'>🗣️ Speak to our AI to order food</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown(
        "<div class='warning-container'><h3 style='color: #EF0606;'>🚨 Voice Chat Not Available</h3><p>Voice chat is disabled due to deployment issues with Streamlit Cloud.</p></div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    ### Why It's Not Working:
    - `streamlit.chat_message` requires Streamlit 1.25.0+, not supported on older cloud versions.
    - `sounddevice` lacks microphone access in cloud environments.
    - `whisper` (STT) requires FFmpeg, which may fail on cloud platforms.
    - `TTS` (Text-to-Speech) depends on `torch`, unavailable on Streamlit Cloud.

    ### 🚀 Run Locally to Enable Voice Chat:
    1. Install **Python 3.10**.
    2. Create a virtual environment:
       ```bash
       python -m venv dinemate_env
       ```
    3. Activate the environment:
       - **Windows**: `dinemate_env\\Scripts\\activate`
       - **macOS/Linux**: `source dinemate_env/bin/activate`
    4. Install dependencies:
       ```bash
       pip install --upgrade pip
       pip install streamlit==1.25.0 torch==2.0.0 torchaudio==2.0.0 TTS whisper pydub sounddevice numpy python-dotenv
       ```
    5. Run the app:
       ```bash
       streamlit run app.py
       ```
    6. Use voice ordering with your microphone! 🎙️
    7. Deactivate: `deactivate`
    """, unsafe_allow_html=True)

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

elif page == "📶 Analysis":
    analysis.show_analysis_page()

# ✅ Logout Button in Sidebar
st.sidebar.divider()
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.success("🚪 Logging out...")
    logger.info({"user": st.session_state["username"], "message": "User logged out"})
    time.sleep(1.2)
    login.logout()