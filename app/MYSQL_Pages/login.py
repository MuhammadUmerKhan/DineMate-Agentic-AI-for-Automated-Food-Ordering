import streamlit as st
from database.MySQL_db import Database
import time

db = Database()

def login():
    """🎯 User Login & Registration Page - Interactive UI"""
    st.markdown(
        "<h1 style='text-align: center; color: #FFA500;'>🔐 Welcome to DineMate</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<h3 style='text-align: center;'>🍽️ Your AI-Powered Food Ordering Assistant</h3>", unsafe_allow_html=True)
    st.divider()

    # ✅ Handle Page Switching
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["page"] == "signup":
        register()
        return

    # ✅ Login Form with Icons 🏆
    st.markdown("### 👤 **User Login**")
    
    # ✅ Username & Password Fields with Toggle Visibility
    col1, col2 = st.columns([2, 2], gap="small")
    with col1:
        username = st.text_input("👨‍💻 Username", key="login_username")
    with col2:
        password = st.text_input("🔑 Password", type="password", key="login_password")

    # ✅ Small Gap Between Buttons (Centered)
    col1, col2 = st.columns([1, 1], gap="small")

    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("🚀 Sign In", use_container_width=True):
            role = db.verify_user(username, password)
            if role:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role
                st.success(f"✅ Welcome, {username}! You are logged in as **{role}**.")
                time.sleep(1.2)  # ⏳ Smooth transition
                st.rerun()
            else:
                st.error("⚠ Incorrect username or password. Please try again!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state["page"] = "signup"
            time.sleep(1.2)  # ⏳ Smooth transition
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='text-align: center;'>🍔 <b>Order faster with AI-powered food ordering!</b></p>", unsafe_allow_html=True)


def register():
    """📝 **User Registration Page - Interactive UI**"""
    st.markdown("<h1 style='text-align: center; color: #28a745;'>📝 Sign Up</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>🚀 Create Your DineMate Account</h3>", unsafe_allow_html=True)
    st.divider()

    # ✅ Input Fields with Side-by-Side Layout
    col1, col2 = st.columns([2, 2], gap="small")
    with col1:
        username = st.text_input("👤 Choose a Username", key="register_username")
    with col2:
        email = st.text_input("📧 Enter Your Email", key="register_email")

    # ✅ Password Field with "Show Password" Toggle
    password = st.text_input("🔒 Choose a Password", type="password", key="register_password")
    
    # ✅ Buttons with Small Gap
    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("✅ Register", use_container_width=True, disabled=not username or not email or not password):
            if not username or not password or not email:
                st.warning("⚠ Please fill in **all fields** to continue.")
                return

            # ✅ Check if username OR email already exists
            existing_user = db.check_existing_user(username, email)
            if existing_user:
                st.error("⚠ Username or Email already exists. Try a different one.")
                return

            # ✅ Register as a "customer"
            success = db.add_user(username, password, email, role="customer")
            if success:
                st.success("🎉 **Registration Successful!** Redirecting to login...")
                st.session_state["page"] = "login"  # ✅ Switch back to login
                time.sleep(1.2)  # ⏳ Smooth transition
                st.rerun()
            else:
                st.error("⚠ Registration failed. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("🔄 Go to Login", use_container_width=True):
            st.session_state["page"] = "login"
            time.sleep(1.2)  # ⏳ Smooth transition
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='text-align: center;'>🔑 Already have an account? Sign in and start ordering delicious food! 🍕</p>", unsafe_allow_html=True)


def logout():
    """🚪 **Log Out the User**"""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.success("🚪 Logging out... Redirecting to Login")
    time.sleep(1.2)  # ⏳ Smooth transition
    st.rerun()
