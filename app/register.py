import streamlit as st
from database.MySQL_db import Database
import time

db = Database()

def register():
    """🎉 **User Registration Page - Modern UI**"""
    st.markdown("<h1 style='text-align: center; color: #28a745;'>📝 Create Your Account</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>🚀 Join DineMate and start ordering delicious food! 🍕</h3>", unsafe_allow_html=True)
    st.divider()

    # ✅ Input Fields with Side-by-Side Layout
    col1, col2 = st.columns([2, 2], gap="small")
    with col1:
        username = st.text_input("👤 Choose a Username")
    with col2:
        email = st.text_input("📧 Enter Your Email")

    password = st.text_input("🔒 Create a Password", type="password")

    # ✅ Buttons with Small Gap
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("✅ Register", use_container_width=True):
            if not username or not password or not email:
                st.warning("⚠ Please fill in **all fields** to continue.")
                return

            # ✅ Check if username OR email already exists
            if db.check_existing_user(username, email):
                st.error("⚠ Username or Email already exists. Try a different one.")
                return

            # ✅ Register user
            success = db.add_user(username, password, email, role="customer")
            if success:
                st.success("🎉 **Registration Successful!** Redirecting to login...")
                st.session_state["register"] = False  # Reset flag
                st.experimental_set_query_params(page="login")  # Redirect to login
                time.sleep(1.2)  # ⏳ Delay for smooth transition
                st.rerun()
            else:
                st.error("⚠ Registration failed. Please try again later.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("🔄 Go to Login", use_container_width=True):
            st.experimental_set_query_params(page="login")
            time.sleep(1.2)  # ⏳ Delay for smooth transition
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='text-align: center;'>🔑 Already have an account? Sign in and start ordering delicious food! 🍔</p>", unsafe_allow_html=True)

# ✅ If on register page, show the registration form
if st.experimental_get_query_params().get("page") == ["register"]:
    register()
