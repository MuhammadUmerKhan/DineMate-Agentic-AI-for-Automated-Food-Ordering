# Import required libraries
import os  # Used for environment variable access
import streamlit as st  # Streamlit for building UI
from streamlit.logger import get_logger  # Streamlit's built-in logger
from langchain_groq import ChatGroq  # Groq API for LLMPI
from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables from .env


# Initialize logger for tracking interactions and errors
logger = get_logger("LangChain-Chatbot")

# ✅ API Key Handling (For Local & Deployed Environments)
grok_api_key = os.getenv("GROK_API_KEY") # Langchain Grok API key (Generate from: https://console.groq.com/)

# Check if API key is available
if not grok_api_key:
    st.error("❌ Missing API Token!")
    st.stop()  # Stop execution if API token is missing

# ✅ Decorator to enable chat history
def enable_chat_history(func):
    """
    Decorator to handle chat history and UI interactions.
    Ensures chat messages persist across interactions.
    """
    current_page = func.__qualname__  # Get function name to track current chatbot session

    # Clear session state if model/chatbot is switched
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page  # Store the current chatbot session
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()  # Clear cached resources
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except Exception:
            pass  # Ignore errors if session state keys do not exist

    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display chat history in the UI
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)  # Execute the decorated function

    return execute


def display_msg(msg, author):
    """
    Displays a chat message in the UI and appends it to session history.

    Args:
        msg (str): The message content to display.
        author (str): The author of the message ("user" or "assistant").
    """
    st.session_state.messages.append({"role": author, "content": msg})  # Store message in session
    st.chat_message(author).write(msg)  # Display message in Streamlit UI


def configure_llm():
    """
    Configure LLM to run on Hugging Face Inference API (Cloud-Based).
    
    Returns:
        llm (LangChain LLM object): Configured model instance.
    """
    # ✅ Use Hugging Face Inference API for cloud execution
    llm = ChatGroq(
    temperature=0.3,
    groq_api_key=grok_api_key,
    model_name="qwen-2.5-32b",
    # system_message="You are an AI assistant. Respond directly and concisely. Do not explain your reasoning unless explicitly asked."
)

    return llm  # Return configured LLM

def print_qa(cls, question, answer):
    """
    Logs the Q&A interaction for debugging and tracking.

    Args:
        cls (class): The calling class.
        question (str): User question.
        answer (str): Model response.
    """
    log_str = f"\nUsecase: {cls.__name__}\nQuestion: {question}\nAnswer: {answer}\n" + "-" * 50
    logger.info(log_str)  # Log the interaction using Streamlit's logger

def sync_st_session():
    """
    Ensures Streamlit session state values are properly synchronized.
    """
    for k, v in st.session_state.items():
        st.session_state[k] = v  # Sync all session state values