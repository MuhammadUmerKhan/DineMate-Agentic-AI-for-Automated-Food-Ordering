import streamlit as st
from FoodBot.bot.main import stream_graph_updates

# Initialize Streamlit app
st.set_page_config(page_title="FoodBot - AI Chatbot", page_icon="🍔", layout="wide")

# Initialize session state for chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🍽️ FoodBot - Your Restaurant Assistant")
st.write("Welcome! Order your favorite meals with our AI-powered chatbot. Type below to begin!")

# Chat message container
chat_container = st.container()

# Display chat history
with chat_container:
    for message in st.session_state.chat_history:
        role, text = message
        with st.chat_message(role):
            st.write(text)

# User input
user_input = st.text_input("Type your message:", key="user_input")

if user_input:
    # Store user input
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)
    
    # Process chatbot response
    bot_response = stream_graph_updates(user_input)
    st.session_state.chat_history.append(("assistant", bot_response))
    
    with st.chat_message("assistant"):
        st.write(bot_response)
