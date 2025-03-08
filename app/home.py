import streamlit as st  # Streamlit for UI

def home():
    """Displays the Home page content with user roles and functionalities."""
    
    # 🎉 Title and Introduction
    st.title("🍽️ DineMate - AI Food Ordering Chatbot")
    st.subheader("Seamless AI-Powered Food Ordering Experience!")

    st.markdown(
        """
        ---
        ## 📌 **Project Overview**
        **DineMate** is an **AI-powered chatbot** that enables users to **order food effortlessly**.  
        With an intelligent chat-based interface, users can:  
        - 🛒 **Browse menu items** and check prices.  
        - 🍔 **Place an order** in natural language.  
        - 🔄 **Modify or replace items** in an existing order.  
        - 🚫 **Cancel an order** within the allowed time.  
        - ⏳ **Track an order** and receive live status updates.  
        - 🤖 **Conversational AI** ensures an engaging user experience.  
        
        Whether you're craving **pizza, burgers, or fresh juice**, DineMate makes food ordering **simple & fun!** 🍕🥤  
        ---

        ## 🏗️ **Who Can Do What? (User Roles & Access)**
        DineMate follows a **role-based access system**, where each user type has specific functionalities:

        ### 👤 **Customers (Users)**
        - ✅ Can access **🏠 Home** and **🍔 DineMate Chatbot** pages.  
        - 🛒 **Place food orders** using the chatbot.  
        - 🔄 **Modify orders** before confirmation.  
        - 🚫 **Cancel orders** within **10 minutes** of placement.  
        - 📦 **Track orders** and check status updates.  

        **Customers CANNOT access:** Kitchen, Order Management, or Admin functionalities.

        ---

        ### 👨‍🍳 **Kitchen Staff (Chefs)**
        - ✅ Can access **👨‍🍳 Kitchen Orders** page.  
        - 📌 **View only non-cancelable orders** (orders placed **10+ minutes ago**).  
        - 🔄 **Update order status** (*e.g., In Process, Ready, Completed*).  

        **Kitchen Staff CANNOT access:** Admin or Customer Support functionalities.

        ---

        ### 📦 **Customer Support Staff**
        - ✅ Can access **📦 Order Management** page.  
        - 📝 **Modify existing orders** (update items, prices, or quantities).  
        - 🚫 **Cancel orders** on behalf of customers (if within allowed time).  

        **Customer Support Staff CANNOT access:** Kitchen or Admin functionalities.

        ---

        ### 🛡️ **Admin (Restaurant Owner / Manager)**
        - ✅ Can access **🛡️ Update Prices** page.  
        - 💰 **Change food item prices** dynamically.  
        - 🛠️ **Manage system functionalities** (e.g., add new items).  

        **Admins CANNOT place orders or manage kitchen operations.**  
        ---

        ## 🚀 **How to Use?**
        Using **DineMate** is simple! Just follow these steps:

        1️⃣ **Go to the chatbot page** (Sidebar → "🍔 DineMate Chatbot")  
        2️⃣ **Start a conversation** – Chat naturally, like:  
            - 📝 *"I want 2 cheeseburgers and 1 Pepsi."*  
            - 🔄 *"Replace my Pepsi with a Mango Smoothie."*  
            - 📦 *"Track my order with ID 33."*  
        3️⃣ **DineMate processes your request**, calculates the total price, and confirms your order.  
        4️⃣ **Track your order** and receive updates on estimated delivery time.  

        DineMate ensures a **fast, reliable, and intelligent** food ordering experience! 🎯  
        ---

        ## 🏗️ **Technologies Used**
        DineMate is built using advanced AI and modern backend technologies:

        - **🧠 AI-Powered Chatbot:**  
          - Uses **Qwen-2.5-32B**, a powerful LLM trained for **food ordering tasks**.  
          - Understands menu queries, order requests, and user modifications.  

        - **🛠️ Backend Technologies:**  
          - **LangChain & LangGraph** – For structured conversation flow and decision-making.  
          - **Python** – AI-powered chatbot logic and order management system.  

        - **📊 Database Management:**  
          - **MySQL** – Stores menu items, order details, and user data.  
          - **Secure Login System** – Uses **hashed passwords** for authentication.  

        - **🌐 Web UI & Integration:**  
          - **Streamlit** – Provides a **clean and interactive UI** for users.  
          - **Session-Based Authentication** – Only allows registered users access.  

        ---

        ## 🔍 **What Happens Behind the Scenes?**
        1️⃣ **User Request Processing:**  
        - Extracts **items & quantities** from chat input.  
        - Checks **menu availability** using **MySQL database**.  

        2️⃣ **Order Processing:**  
        - Stores **orders in memory** until confirmed.  
        - Calculates **total price dynamically**.  

        3️⃣ **Order Tracking & Status Updates:**  
        - Fetches **real-time order status** from the database.  
        - Displays estimated delivery time dynamically.  

        ---

        ## 🔗 **Project Repository & Contributions**
        **View Source Code:** [GitHub Repository](https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot)  
        Built with ❤️ by **Muhammad Umer Khan**  

        ---
        """,
        unsafe_allow_html=True
    )

    # 📌 Footer
    st.markdown("© 2025 **DineMate AI** | Built with ❤️ by **Muhammad Umer Khan**")
