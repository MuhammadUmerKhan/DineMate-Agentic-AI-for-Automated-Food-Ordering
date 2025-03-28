import streamlit as st  # Streamlit for UI

def home():
    """🏠 Displays the Home page with user roles, features, and how-to guide."""
    
    # 🎉 Title and Introduction
    st.markdown("""
        <h1 style='text-align: center; color: #C70039;'>🍽️ Welcome to DineMate</h1>
        <h3 style='text-align: center;'>🚀 AI-Powered Smart Food Ordering & Business Analytics</h3>
    """, unsafe_allow_html=True)
    st.divider()

    # 📌 **Project Overview**
    with st.expander("📌 **About DineMate**", expanded=True):
        st.markdown("""
        **DineMate** is an **AI-driven food ordering system** that automates restaurant operations. 
        It provides a conversational **AI chatbot** for seamless order placement, real-time tracking, 
        and intelligent recommendations. 🚀
        
        **Key Features:**
        - 🛒 **Browse menu & dynamic pricing**
        - 🍔 **Order via natural conversation**
        - 🔄 **Modify or replace items**
        - 🚫 **Smart order cancellations (within 10 min)**
        - 📦 **Real-time order tracking**
        - 📊 **Business analytics dashboard**
        - 🗣️ **Voice DineMate – Voice-enabled ordering system**
        """)
    
    # 🆕 **New Functionalities**
    with st.expander("🛠️ **Key Features?**", expanded=True):
        st.markdown("""
        🚀 **Recent Enhancements:**
        - 📦 **Live Order Tracking** – Customers can now track their orders in real time!  
        - 🛒 **Add/Remove Menu Items** – Admins can **add new dishes** or **remove outdated items**.  
        - 💰 **Dynamic Price Management** – Admins can **adjust menu prices dynamically**.  
        - 🔄 **Customer Support Panel** – Staff can now **cancel or modify orders**.  
        - 👨‍🍳 **Kitchen Dashboard** – Kitchen staff get **a dedicated panel** to manage orders.  
        - 📊 **Business Analytics** – Monitor revenue, peak order times & demand trends.  
        - 🗣️ **Voice DineMate** – **Order food using voice commands!**
        """)
    
    # 🎤 **Voice DineMate - AI Voice Ordering System**
    with st.expander("🎤 **Introducing Voice DineMate!**", expanded=True):
        st.markdown("""
        🚀 **Now, order your favorite food with just your voice!**  
        **Voice DineMate** uses advanced **Speech-to-Text (STT) and Text-to-Speech (TTS)** technology to let customers 
        interact with the chatbot hands-free. 🎙️
        
        **How It Works?**
        
        1️⃣ **Enable voice mode** in the chatbot panel.  
        2️⃣ **Speak naturally** – Example: *"I want a chicken burger with fries."*  
        3️⃣ **The AI processes your voice command** and places the order.  
        4️⃣ **Get real-time voice responses** with order confirmation and tracking.  
        """)
    
    # 🏗️ **User Roles & Access**
    with st.expander("🏗️ **User Roles & Permissions**", expanded=True):
        role_data = {
            "👤 Customers": [
                "✅ Order food using chatbot or voice commands",
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
    
    # 🚀 **How to Use?**
    with st.expander("🚀 **How to Use DineMate?**", expanded=True):
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
    
    # 🏗️ **Technologies Used**
    with st.expander("🏗️ **Technologies Used**", expanded=True):
        tech_data = {
            "🧠 AI-Powered Chatbot": "Uses **Qwen-2.5-32B**, an advanced LLM for food ordering.",
            "🛠️ Backend Technologies": "Built with **LangChain & LangGraph** for structured chatbot interactions.",
            "📊 Database Management": "Stores order details securely in **MySQL**.",
            "🌐 Web UI": "Interactive UI powered by **Streamlit**.",
            "🎤 Voice Processing": "Uses **Whisper AI** for **Speech-to-Text (STT)** & **TTS APIs** for responses."
        }

        for tech, desc in tech_data.items():
            st.markdown(f"<h3 style='color: #6C757D;'>{tech}</h3>", unsafe_allow_html=True)
            st.markdown(f"✔ {desc}")
    
    # 🔍 **What Happens Behind the Scenes?**
    with st.expander("🔍 **How DineMate Works?**", expanded=True):
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
    
    # 🔗 **Project Repository**
    
    st.markdown("""
    <h2 style='color: #343A40;'>🔗 View Source Code</h2>
    <p>
        <a href='https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot' 
           target='_blank' style='text-decoration: none; color: #007BFF; font-weight: bold;'>
            🌍 GitHub Repository </a> - Built with ❤️ by Muhammad Umer Khan
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>© 2025 <b>DineMate AI</b> | Powered by ❤️</p>", unsafe_allow_html=True)
