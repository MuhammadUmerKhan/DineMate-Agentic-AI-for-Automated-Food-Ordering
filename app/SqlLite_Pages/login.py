import streamlit as st
from database.SQLLITE_db import Database
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

    # ✅ Show Demo Credentials (For Testing Purposes)
    with st.expander("🔑 **Demo Login Credentials (Click to Expand)**"):
        st.markdown("""
        - 👨‍💼 **Admin**  
          - **Username:** `admin`  
          - **Password:** `admin123`  

        - 🛠 **Support Staff**  
          - **Username:** `support`  
          - **Password:** `support123`  

        - 👨‍🍳 **Chef (Kitchen Staff)**  
          - **Username:** `chef`  
          - **Password:** `chef123`  

        - 👤 **Customer:** Please **sign up** to create an account.
        """, unsafe_allow_html=True)

    with st.expander("🔑 **Read Instructions (Click to Expand)**"):
        st.markdown("""
        ### 🍽️ **Welcome to DineMate - Your AI-Powered Food Ordering Assistant!**
        DineMate allows you to **order food, track your orders, manage the kitchen, update prices, and more**. Below are the instructions on how to use the system effectively.

        ---
        ### 🏠 **Home Page**
        - 📌 **View General Information** about DineMate before logging in.
        - 🔐 **Sign Up or Log In** to access your assigned dashboard.

        ---
        ### 🔐 **Login & Sign-Up Instructions**
        - **For Customers** → Sign up with a username, email, and password.
        - **For Admin, Kitchen Staff, & Customer Support** → Use predefined credentials.
        - **Forgot credentials?** Contact the system administrator.

        ---
        ### 🍔 **For Customers**
        - 🤖 **DineMate Chatbot** → Order food by chatting with the AI.
        - 📦 **Track Order** → Check your order status in real-time.
    
        ---
        ### 👨‍🍳 **For Kitchen Staff**
        - 📦 **Kitchen Orders** → View only **orders that cannot be canceled**.
        - 🔄 **Update Order Status** → Change the status of an order as it progresses.

        ---
        ### 🛡️ **For Admins**
        - 💰 **Update Prices** → Modify menu item prices.
        - ➕ **Add/Remove Items** → Add new food items or remove existing ones.
        - 📦 **Order Management** → Modify, cancel, or update any order.

        ---
        ### 📞 **For Customer Support**
        - 📦 **Order Management** → Modify orders, cancel orders, or update order status.

        ---
        ### 🔄 **How Orders Work?**
        1. Customers place an order via the **DineMate Chatbot**.
        2. The order is stored in the system and can be **modified or canceled** within 10 minutes.
        3. After **10 minutes**, orders appear for the **kitchen staff** (cannot be canceled).
        4. Kitchen staff updates the **order status** as it progresses.
        5. Once **completed**, the order status changes to **Delivered**.

        ---
        ### 🔑 **Additional Notes**
        - 🚀 **Orders older than 10 minutes appear automatically for the kitchen staff.**
        - ✅ **Admins can modify any order, update prices, and manage the menu.**
        - 📦 **Customer support can assist in modifying or canceling orders.**
        - 🔄 **The system auto-refreshes to display new orders when they are ready.**
    """)
    
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
        if st.button("✅ Register", use_container_width=True):
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
