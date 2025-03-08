import streamlit as st  # Streamlit for UI

def home():
    """Displays the Home page content with user roles and functionalities."""

    # 🎉 Title and Introduction
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>🍽️ Welcome to DineMate</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>🚀 Your AI-Powered Smart Food Ordering System</h3>", unsafe_allow_html=True)
    st.divider()

    # 📌 **Project Overview**
    st.markdown("<h2 style='color: #007BFF;'>📌 About DineMate</h2>", unsafe_allow_html=True)
    st.markdown("""
        **DineMate** is an **AI-powered chatbot** that makes **food ordering seamless and intelligent**.  
        It offers an interactive **conversational experience** where users can:  
        - 🛒 **Browse menu items & prices**.  
        - 🍔 **Place orders** via natural conversation.  
        - 🔄 **Modify or replace items** in an existing order.  
        - 🚫 **Cancel orders** within 10 minutes of placement.  
        - 📦 **Track orders in real time** with delivery status updates.  
        - 🤖 **Get intelligent recommendations** for meals.  
        - 🛠️ **Admins can update menu prices & manage inventory.**  
        
        Whether you're craving **pizza, burgers, or fresh juice**, DineMate makes ordering **fast & fun!** 🍕🥤  
    """)

    st.divider()

    # 🆕 **New Functionalities**
    st.markdown("<h2 style='color: #D63384;'>🆕 What’s New in DineMate?</h2>", unsafe_allow_html=True)
    st.markdown("""
        🚀 **Recent Enhancements:**  
        - 📦 **Order Tracking** – Customers can now track their orders in real time!  
        - 🛒 **Add/Remove Menu Items** – Admins can **add new dishes** or **remove outdated items**.  
        - 💰 **Price Update System** – Admins can now **adjust menu prices dynamically**.  
        - 🔄 **Customer Support Panel** – Support staff can now **cancel orders or modify order items**.  
        - 👨‍🍳 **Kitchen Dashboard** – Kitchen staff get **a dedicated panel** to view & manage orders.  
    """)

    st.divider()

    # 🏗️ **User Roles & Access**
    st.markdown("<h2 style='color: #28A745;'>🏗️ User Roles & Permissions</h2>", unsafe_allow_html=True)

    role_data = {
        "👤 Customers": [
            "✅ Order food using chatbot",
            "✅ Modify/cancel orders (within time limits)",
            "✅ Track orders in real time"
        ],
        "👨‍🍳 Kitchen Staff": [
            "✅ View only non-cancelable orders (10+ minutes old)",
            "✅ Update order status"
        ],
        "📦 Customer Support": [
            "✅ Modify existing orders",
            "✅ Cancel orders on behalf of customers"
        ],
        "🛡️ Admin": [
            "✅ Add/remove menu items",
            "✅ Change food item prices",
            "✅ Manage system functionalities"
        ]
    }

    for role, permissions in role_data.items():
        st.markdown(f"<h3 style='color: #DC3545;'>{role}</h3>", unsafe_allow_html=True)
        for perm in permissions:
            st.markdown(f"✔ {perm}")

    st.divider()

    # 🚀 **How to Use?**
    st.markdown("<h2 style='color: #FFC107;'>🚀 How to Use DineMate?</h2>", unsafe_allow_html=True)
    st.markdown("""
        **Ordering is easy! Just follow these steps:**  
        1️⃣ **Go to the chatbot page** (Sidebar → "🍔 DineMate Chatbot")  
        2️⃣ **Start a conversation** – Chat naturally, like:  
        - 📝 *"I want 2 cheeseburgers and 1 Pepsi."*  
        - 🔄 *"Replace my Pepsi with a Mango Smoothie."*  
        - 📦 *"Track my order with ID 33."*  
        3️⃣ **DineMate processes your request**, calculates the total price, and confirms your order.  
        4️⃣ **Track your order** and receive updates on estimated delivery time.  
    """)

    st.divider()

    # 🏗️ **Technologies Used**
    st.markdown("<h2 style='color: #17A2B8;'>🏗️ Technologies Used</h2>", unsafe_allow_html=True)
    tech_data = {
        "🧠 AI-Powered Chatbot": "Uses **Qwen-2.5-32B**, an advanced LLM for handling food orders.",
        "🛠️ Backend Technologies": "Uses **LangChain & LangGraph** for structured chatbot interactions.",
        "📊 Database Management": "Stores order details securely in **MySQL**.",
        "🌐 Web UI": "Interactive UI powered by **Streamlit**."
    }

    for tech, desc in tech_data.items():
        st.markdown(f"<h3 style='color: #6C757D;'>{tech}</h3>", unsafe_allow_html=True)
        st.markdown(f"✔ {desc}")

    st.divider()

    # 🔍 **What Happens Behind the Scenes?**
    st.markdown("<h2 style='color: #6C757D;'>🔍 How DineMate Works?</h2>", unsafe_allow_html=True)
    st.markdown("""
        1️⃣ **User Request Processing:**  
        - Extracts **items & quantities** from chat input.  
        - Checks **menu availability** using **MySQL database**.  

        2️⃣ **Order Processing:**  
        - Stores **orders in memory** until confirmed.  
        - Calculates **total price dynamically**.  

        3️⃣ **Order Tracking & Status Updates:**  
        - Fetches **real-time order status** from the database.  
        - Displays estimated delivery time dynamically.  
    """)

    st.divider()

    # 🔗 **Project Repository**
    st.markdown("<h2 style='color: #343A40;'>🔗 View Source Code</h2>", unsafe_allow_html=True)
    st.markdown("[GitHub Repository](https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot) - Built with ❤️ by **Muhammad Umer Khan**")

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2025 **DineMate AI** | Powered by ❤️</p>", unsafe_allow_html=True)
