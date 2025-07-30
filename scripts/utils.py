# Import required libraries

from dotenv import load_dotenv
from langsmith import traceable
import streamlit as st
from scripts.logger import get_logger
from scripts.config import GROQ_API_KEY, LANGCHAIN_PROJECT, DEFAULT_MODEL_NAME
from langchain_groq import ChatGroq

load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Check if API key is available
if not GROQ_API_KEY:
    st.error("❌ Missing API Token!")
    st.stop()

# Decorator to enable chat history
def enable_chat_history(func):
    """
    Decorator to handle chat history and UI interactions.
    Ensures chat messages persist across interactions.
    """
    current_page = func.__qualname__

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except Exception:
            pass

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help?"}]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute

def display_msg(msg, author):
    """
    Displays a chat message in the UI and appends it to session history.

    Args:
        msg (str): The message content to display.
        author (str): The author of the message ("user" or "assistant").
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

@st.cache_resource
@traceable(run_type="llm", project_name=LANGCHAIN_PROJECT)
def configure_llm(DEFAULT_MODEL_NAME=DEFAULT_MODEL_NAME):
    """
    Configure LLM to run on Hugging Face Inference API (Cloud-Based).
    
    Returns:
        llm (LangChain LLM object): Configured model instance.
    """
    llm = ChatGroq(
        temperature=0.3,
        groq_api_key=GROQ_API_KEY,
        model_name=DEFAULT_MODEL_NAME,
        max_tokens=100  # Limit response length
    )
    logger.info("🤖 LLM configured")
    return llm

def print_qa(cls, question, answer):
    """
    Logs the Q&A interaction for debugging and tracking.

    Args:
        cls (class): The calling class.
        question (str): User question.
        answer (str): Model response.
    """
    log_str = f"\nUsecase: {cls.__name__}\nQ: {question}\nA: {answer}\n" + "-" * 50
    logger.info("💬 Q&A logged")

def sync_st_session():
    """
    Ensures Streamlit session state values are properly synchronized.
    """
    for k, v in st.session_state.items():
        st.session_state[k] = v