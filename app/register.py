"""
# DineMate Registration 📝

This module handles user registration for DineMate.

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
db = Database()

# ✅ Load centralized CSS
try:
    with open(STATIC_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

def register():
    st.markdown(
        "<div class='header'><h1>📝 Create Your Account</h1><p style='color: #E8ECEF;'>🚀 Join DineMate and start ordering delicious food! 🍕</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    col1, col2 = st.columns([2, 2], gap="small")
    with col1:
        username = st.text_input("👤 Choose a Username", placeholder="Enter username", help="Your unique username")
    with col2:
        email = st.text_input("📧 Enter Your Email", placeholder="Enter email", help="Your email address")

    password = st.text_input("🔒 Create a Password", type="password", placeholder="Enter password", help="Choose a secure password")

    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        if st.button("✅ Register", width="stretch"):
            if not username or not password or not email:
                st.warning("⚠ Please fill in **all fields** to continue.")
                logger.warning({"message": "Incomplete registration fields"})
                return

            if db.check_existing_user(username, email):
                st.error("⚠ Username or Email already exists. Try a different one.")
                logger.warning({"username": username, "email": email, "message": "User/email exists"})
                return

            success = db.add_user(username, password, email, role="customer")
            if success:
                st.success("🎉 **Registration Successful!** Redirecting to login...")
                logger.info({"username": username, "email": email, "message": "User registered"})
                st.session_state["register"] = False
                st.experimental_set_query_params(page="login")
                time.sleep(1.2)
                st.rerun()
            else:
                st.error("⚠ Registration failed. Please try again later.")
                logger.error({"username": username, "email": email, "message": "Registration failed"})

    with col2:
        if st.button("🔄 Go to Login", width="stretch"):
            st.experimental_set_query_params(page="login")
            time.sleep(1.2)
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center;'>🔑 Already have an account? Sign in and start ordering delicious food! 🍔</p>", unsafe_allow_html=True)

if st.experimental_get_query_params().get("page") == ["register"]:
    register()