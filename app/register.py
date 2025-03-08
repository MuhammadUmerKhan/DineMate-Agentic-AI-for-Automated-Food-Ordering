import streamlit as st
from database.db import Database
import time

db = Database()

def register():
    """✅ User Registration Page."""
    st.title("📝 Create a New Account")

    username = st.text_input("Choose a Username")
    email = st.text_input("Email")
    password = st.text_input("Create a Password", type="password")

    if st.button("Register"):
        if not username or not password or not email:
            st.warning("⚠ Please fill in all fields.")
            return
        
        # ✅ Check if username/email already exists
        if db.check_existing_user(username, email):
            st.error("⚠ Username or Email already exists. Try a different one.")
            return

        # ✅ Register user
        success = db.add_user(username, password, email, role="customer")
        if success:
            st.success("✅ Registration successful! Redirecting to login...")
            st.session_state["register"] = False  # Reset flag
            st.experimental_set_query_params(page="login")  # Redirect to login
            time.sleep(1.2)  # ⏳ Delay for 2 seconds
            st.rerun()
        else:
            st.error("⚠ Registration failed. Try again later.")

# ✅ If on register page, show the registration form
if st.experimental_get_query_params().get("page") == ["register"]:
    register()