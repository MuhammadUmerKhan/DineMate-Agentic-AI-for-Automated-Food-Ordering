"""
# DineMate Login and Registration 🔐

This module handles user authentication and registration for DineMate.

Dependencies:
- streamlit: For UI rendering 📺.
- db: For database operations 🗄️.
- logger: For structured logging 📜.
"""

import streamlit as st
from scripts.db import Database
from scripts.logger import get_logger
from scripts.config import STATIC_CSS_PATH
import time

logger = get_logger(__name__)

# ✅ Load centralized CSS
try:
    with open(STATIC_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

def login() -> None:
    """🔐 Display the user login and registration page."""
    st.markdown(
        "<div class='header'><h1>🔐 Welcome to DineMate</h1><p style='color: #E8ECEF;'>🍽️ Your AI-Powered Food Ordering Assistant</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    # 📋 Demo Credentials
    with st.expander("🔑 Demo Login Credentials", expanded=False):
        st.markdown("""
        - 👨‍💼 **Admin**: `admin` / `admin123`
        - 👨‍🍳 **Kitchen Staff**: `kitchen` / `kitchen123`
        - 📞 **Customer Support**: `support` / `support123`
        - 👤 **Customer**: `customer` / `customer123`
        - ❗ **Troubleshooting**: If you face issues signing up, use `umer` / `umer123` to sign in.
        """)

    # 📜 Instructions
    with st.expander("📜 Instructions", expanded=False):
        st.markdown("""
        ### 🍽️ Welcome to DineMate!
        - **Customers**: Sign up or use the chatbot to order food 🍔.
        - **Staff**: Use demo credentials to log in 👨‍🍳.
        - **Orders**: Modify/cancel within 10 minutes; kitchen staff see orders after 10 minutes 📦.
        - **Admins**: Manage menu items and prices 🛡️.
        - **Support**: Assist with order modifications 📞.
        """, unsafe_allow_html=True)

    # 🔄 Page Switching
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["page"] == "signup":
        register()
        return

    # 👤 Login Form
    st.markdown("### 👤 User Login")
    col1, col2 = st.columns([2, 2], gap="small")
    with col1:
        username = st.text_input("👨‍💻 Username", key="login_username", placeholder="Enter username", help="Your unique username")
    with col2:
        password = st.text_input("🔑 Password", type="password", key="login_password", placeholder="Enter password", help="Your secure password")

    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        if st.button("🚀 Sign In", use_container_width=True):
            with st.spinner("⏳ Logging in..."):
                db = Database()
                try:
                    role = db.verify_user(username, password)
                    if role:
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.session_state["role"] = role
                        st.success(f"✅ Welcome, {username}! Logged in as {role}.")
                        logger.info({"username": username, "role": role, "message": "User logged in"})
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("⚠ Incorrect username or password.")
                        logger.warning({"username": username, "message": "Login failed"})
                finally:
                    db.close_connection()

    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state["page"] = "signup"
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center;'>🍔 <b>Order smarter with DineMate!</b></p>", unsafe_allow_html=True)

def register() -> None:
    """📝 Display the user registration page."""
    st.markdown(
        "<div class='header'><h1>📝 Sign Up</h1><p style='color: #E8ECEF;'>🚀 Create Your DineMate Account</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    col1, col2 = st.columns([2, 2], gap="small")
    with col1:
        username = st.text_input("👤 Username", key="register_username", placeholder="Enter username", help="Choose a unique username")
    with col2:
        email = st.text_input("📧 Email", key="register_email", placeholder="Enter email", help="Your email address")
    password = st.text_input("🔒 Password", type="password", key="register_password", placeholder="Enter password", help="Choose a secure password")

    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        if st.button("✅ Register", use_container_width=True):
            with st.spinner("⏳ Registering..."):
                if not (username and password and email):
                    st.warning("⚠ Please fill all fields.")
                    logger.warning({"message": "Incomplete registration fields"})
                    return
                db = Database()
                try:
                    if db.check_existing_user(username, email):
                        st.error("⚠ Username or email already exists.")
                        logger.warning({"username": username, "email": email, "message": "User/email exists"})
                        return
                    if db.add_user(username, password, email, role="customer"):
                        st.success("🎉 Registration successful! Redirecting to login...")
                        logger.info({"username": username, "email": email, "message": "User registered"})
                        st.session_state["page"] = "login"
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("⚠ Registration failed.")
                        logger.error({"username": username, "email": email, "message": "Registration failed"})
                finally:
                    db.close_connection()

    with col2:
        if st.button("🔄 Go to Login", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center;'>🔑 Already have an account? Sign in! 🍕</p>", unsafe_allow_html=True)

def logout() -> None:
    """🚪 Log out the user and clear session state."""
    logger.info({"username": st.session_state.get("username"), "message": "User logging out"})
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.session_state["page"] = "login"
    st.success("🚪 Logged out. Redirecting to login...")
    time.sleep(0.5)
    st.rerun()