import streamlit as st  # Streamlit for UI
import scripts.utils as utils  # Utility functions for chatbot and session handling
from scripts.streaming import StreamHandler  # Handles real-time streaming responses
from scripts.streaming import stream_graph_updates  # Function to process chatbot responses
from app import kitchen  # Import Kitchen page
from app import update_prices  # Import Admin page for updating item prices
from app import login  # Import authentication system
from app import order_management  # Import Order Management page
from app import home  # Import Home page
from app import add_remove_items  # Import Add/Remove Items Page
from app import track_order  # Import Order Tracking Page
from app import analysis  # Import Analysis Page
# from app import voice_chat  # Import Voice Chat with DineMate
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
    "customer": ["🏠 Home", "🍔 DineMate Chatbot", "🎙️ Voice Chat", "📦 Track Order"]  
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
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>🤖 DineMate Chatbot</h1>", unsafe_allow_html=True)
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
                    response = stream_graph_updates(user_query=user_query, thread_id=1)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    utils.print_qa(chatbot_main, user_query, response)

                except Exception as e:
                    error_msg = f"⚠ Error processing request: {str(e)}"
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    chatbot_main()  # ✅ Run chatbot

elif page == "🎙️ Voice Chat":
    st.markdown("<h1 style='text-align: center; color: #01877e'>🎙️ Voice Chat with DineMate</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>🗣️ Your AI-Powered Voice Ordering Assistant</p>", unsafe_allow_html=True)
    
    # @utils.enable_chat_history
    # def voice_order():
    #     if "recording" not in st.session_state:
    #         st.session_state["recording"] = False

    #     # Start Conversation Button
    #     if st.button("🎤 Start AI Conversation"):
    #         st.session_state["recording"] = True

    #     # Stop Conversation Button
    #     if st.button("⛔ Stop Conversation"):
    #         st.session_state["recording"] = False

    #     # 🔄 Continuous AI Chat Loop
    #     while st.session_state["recording"]:
    #         audio_file = voice_chat.record_audio()
    #         user_query = voice_chat.transcribe_audio(audio_file)

    #         if user_query:
    #             utils.display_msg(user_query, "user")
    #             with st.chat_message("assistant"):
    #                 st_sb = StreamHandler(st.empty())

    #                 try:
    #                     response = voice_chat.get_llm_response(user_query)
    #                     st.write(response)
    #                     st.session_state.messages.append({"role": "assistant", "content": response})
    #                     utils.print_qa(voice_order, user_query, response)
    #                     # Convert AI response to speech and play it
    #                     response_audio = voice_chat.text_to_speech(response)
    #                     # st.audio(response_audio, format="audio/wav")
    #                 except Exception as e:
    #                     error_msg = f"⚠ Error processing request: {str(e)}"
    #                     st.write(error_msg)
    #                     st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
    #         # ✅ Add a small delay to prevent system overload
    #         time.sleep(1)

    #         # 🔴 Stop loop if user presses "Stop Conversation"
    #         if not st.session_state["recording"]:
    #             break
    # voice_order()
    
    # 📌 Highlight Deployment Issues
    st.markdown("<h2 style='text-align: center; color: #ef0606;'>🚨 Deployment Not Done Due to Library Version Issues</h2>", unsafe_allow_html=True)
    st.markdown("""

    This project **cannot be deployed** on Streamlit Cloud due to the following reasons:

    - `streamlit.chat_message` **requires Streamlit 1.25.0+**, but deployment supports older versions.
    - `sounddevice` may not work properly in cloud environments due to microphone access restrictions.
    - `whisper` (OpenAI's STT model) requires **FFmpeg** and might fail on certain cloud platforms.
    - `TTS` (Torch-based Text-to-Speech) has dependencies on `torch` and GPU acceleration, which is **not available on Streamlit Cloud**.

    ### ✅ Solution: Run Locally
    Follow the instructions below to set up and run the app on your local machine.
    """)
    # 📌 Instructions to Use Locally
    st.markdown("""
    ### 🚀 How to Run Locally:
    1️⃣ **Install Python 3.10** if not installed.
    2️⃣ **Create a Virtual Environment:**
    ```bash
    python -m venv dinemate_env
    ```
    3️⃣ **Activate the Virtual Environment:**
    - **Windows:** `dinemate_env\Scripts\activate`
    - **macOS/Linux:** `source dinemate_env/bin/activate`
    4️⃣ **Install Required Libraries:**
    ```bash
    pip install --upgrade pip
    pip install streamlit==1.25.0 torch==2.0.0 torchaudio==2.0.0 TTS whisper pydub sounddevice numpy python-dotenv coqui-ai-tts
    ```
    5️⃣ **Run Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    6️⃣ **Use the AI Voice Ordering System!** 🎙️ <br>
    7️⃣ **Deactivate Environment When Done:** `deactivate`
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

# ✅ **Logout Button in Sidebar**
st.sidebar.divider()
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.success("🚪 Logging out... Redirecting to Login Page")
    time.sleep(1.2)  # ⏳ Delay for a smooth transition
    login.logout()
