import streamlit as st  # Streamlit for UI
import utils  # Utility functions for chatbot and session handling
from streaming import StreamHandler  # Handles real-time streaming responses
from bot.agent import stream_graph_updates  # Function to process chatbot responses
from app.SqlLite_Pages import kitchen  # Import Kitchen page
from app.SqlLite_Pages import update_prices  # Import Admin page for updating item prices
from app.SqlLite_Pages import login  # Import authentication system
from app.SqlLite_Pages import order_management  # Import Order Management page
from app.SqlLite_Pages import home  # Import Home page
from app.SqlLite_Pages import add_remove_items  # Import Add/Remove Items Page
from app.SqlLite_Pages import track_order  # Import Order Tracking Page
from app.SqlLite_Pages import analysis  # Import Analysis Page
from app.SqlLite_Pages import voice_chat  # Import Voice Chat with DineMate
import time

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

# 🎨 **Stylish Sidebar - Navigation with Emojis**
st.sidebar.markdown("<h2 style='text-align: center;'>📌 Navigation</h2>", unsafe_allow_html=True)
st.sidebar.markdown(
    f"<h3>👋 Welcome, <span style='color: #FFA500;'>{st.session_state['username'].title()}</span>!</h3>",
    unsafe_allow_html=True
)

# ✅ Define Role-Based Page Access (Each role gets only their assigned pages)
ROLE_PAGES = {
    "admin": ["🏠 Home", "🛡️ Update Prices", "👨‍🍳 Kitchen Orders", "➕ Add/Remove Items", "📶 Analysis"],  
    "kitchen_staff": ["🏠 Home", "👨‍🍳 Kitchen Orders"],  
    "customer_support": ["🏠 Home", "📦 Order Management"],  
    "customer": ["🏠 Home", "🍔 DineMate Chatbot", "🎙️ Voice Chat with DineMate", "📦 Track Order"]  
}

# ✅ Get allowed pages for the logged-in role
available_pages = ROLE_PAGES.get(st.session_state["role"], [])

# 🚨 **If No Assigned Pages, Show Warning**
if not available_pages:
    st.sidebar.warning("⚠ You do not have access to any pages.")
    st.stop()

# ✅ Sidebar Navigation Menu
page = st.sidebar.radio("📌 **Select a Page:**", available_pages)

# 🎯 **Load Selected Page**
if page == "🏠 Home":
    home.home()

elif page == "🍔 DineMate Chatbot":
    st.markdown("<h1 style='text-align: center;'>🤖 DineMate Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>🍽️ Your AI-Powered Food Ordering Assistant</p>", unsafe_allow_html=True)
    st.divider()

    # ✅ Enable Chat History
    @utils.enable_chat_history
    def chatbot_main():
        """Main function to handle chatbot interactions."""
        user_query = st.chat_input(placeholder="💬 Type your food order or ask a question...")

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

elif page == "🎙️ Voice Chat with DineMate":
    st.markdown("<h1 style='text-align: center;'>🎙️ Voice Chat with DineMate</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>🗣️ Your AI-Powered Voice Ordering Assistant</p>", unsafe_allow_html=True)
    
    @utils.enable_chat_history
    def voice_order():
        if "recording" not in st.session_state:
            st.session_state["recording"] = False

        # Start Conversation Button
        if st.button("🎤 Start AI Conversation"):
            st.session_state["recording"] = True

        # Stop Conversation Button
        if st.button("⛔ Stop Conversation"):
            st.session_state["recording"] = False

        # 🔄 Continuous AI Chat Loop
        while st.session_state["recording"]:
            audio_file = voice_chat.record_audio()
            user_query = voice_chat.transcribe_audio(audio_file)

            if user_query:
                utils.display_msg(user_query, "user")
                with st.chat_message("assistant"):
                    st_sb = StreamHandler(st.empty())

                    try:
                        response = voice_chat.get_llm_response(user_query)
                        st.write(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        utils.print_qa(voice_order, user_query, response)
                        # Convert AI response to speech and play it
                        response_audio = voice_chat.text_to_speech(response)
                        # st.audio(response_audio, format="audio/wav")
                    except Exception as e:
                        error_msg = f"⚠ Error processing request: {str(e)}"
                        st.write(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            # ✅ Add a small delay to prevent system overload
            time.sleep(1)

            # 🔴 Stop loop if user presses "Stop Conversation"
            if not st.session_state["recording"]:
                break
    voice_order()

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

# ✅ **Logout Button in Sidebar**
st.sidebar.divider()
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.success("🚪 Logging out... Redirecting to Login Page")
    time.sleep(1.2)  # ⏳ Delay for a smooth transition
    login.logout()
