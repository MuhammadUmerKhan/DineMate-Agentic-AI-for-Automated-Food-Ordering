import streamlit as st  # Streamlit for UI
import utils  # Utility functions for chatbot and session handling
from streaming import StreamHandler  # Handles real-time streaming responses
from bot.agent import stream_graph_updates  # Function to process chatbot responses
from app.home import home  # Import Home page for navigation
from app import kitchen  # Import Kitchen page for tracking orders

# ✅ Set up Streamlit UI
st.set_page_config(page_title="DineMate - Food Ordering Bot", page_icon="🍽️", layout="wide")
# st.write("Welcome! You can order food, track your order, and more.")

# ✅ Sidebar Navigation
page = st.sidebar.radio("📌 Select Page", ["🏠 Home", "🍔 DineMate Chatbot", "👨‍🍳 Kitchen Orders"])

# 🎯 Load Home Page
if page == "🏠 Home":
    home()
elif page == "👨‍🍳 Kitchen Orders":
    kitchen.show_kitchen_orders()
elif page == "🍔 DineMate Chatbot":
    st.title("🍽️ DineMate - AI Food Ordering Chatbot")
    # ✅ Display GitHub Source Code Button
    st.write('[![View Source Code](https://img.shields.io/badge/view_source_code-gray?logo=github)]'
             '(https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot)')

    # ✅ Enable Chat History
    @utils.enable_chat_history
    def main():
        """Main function to handle chatbot interactions."""

        user_query = st.chat_input(placeholder="Ask me anything about food ordering!")

        if user_query:  # If user provides input
            utils.display_msg(user_query, "user")  # Display user's message in UI

            with st.chat_message("assistant"):  # Display assistant's response
                st_sb = StreamHandler(st.empty())  # Create streaming handler for live updates

                try:
                    # ✅ Process the user query using LangChain graph
                    response = stream_graph_updates(user_query)

                    # ✅ Unicode-safe decoding
                    # response = response.encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore')

                    # ✅ Display response in Streamlit
                    st.write(response)

                    # ✅ Store response in session history
                    st.session_state.messages.append({"role": "assistant", "content": response})

                    # ✅ Log the interaction
                    utils.print_qa(main, user_query, response)

                except Exception as e:
                    error_msg = f"⚠ Error processing request: {str(e)}"
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # ✅ Run the chatbot application
    if __name__ == "__main__":
        main()
