import streamlit as st  # Streamlit for UI

def show_home():
    """Displays the Home page content."""
    
    # ✅ Set up Streamlit UI
    # st.set_page_config(page_title="DineMate - Home", page_icon="🍽️", layout="wide")

    # 🎉 Title and Intro
    st.title("🍽️ DineMate - AI Food Ordering Chatbot")
    st.subheader("Seamless AI-Powered Food Ordering Experience!")

    st.markdown(
        """
        ---
        ## 📌 **Project Overview**
        **DineMate** is an advanced AI-powered chatbot designed to **simplify online food ordering**.  
        With an **interactive and human-like chat interface**, users can:
        - 🛒 **Browse the menu** and explore available food items.
        - 🍔 **Place an order** using natural language.
        - 🔄 **Modify or replace items** in an existing order.
        - 🚫 **Cancel an order** before or after confirmation (within time limits).
        - ⏳ **Track an order** in real time, including delivery estimates.
        - 🧠 **Intelligently handle user requests**, focusing on food-related conversations.

        Whether you're craving **pizza, burgers, or fresh juice**, DineMate makes **food ordering effortless and fun!** 🍕🥤
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
        DineMate leverages cutting-edge AI and software engineering practices:

        - **🧠 LLM (Large Language Model):**  
          - Uses **Qwen-2.5-32B**, a powerful AI model trained for conversational tasks.  
          - Understands food-related queries and intelligently manages orders.  

        - **🛠️ Backend Technologies:**  
          - **LangChain** – A framework that connects LLM with external tools (like databases).  
          - **LangGraph** – Handles conversation flow, decision-making, and tool execution.  
          - **Python** – Custom-built AI agent and order management system.  

        - **📊 Database Management:**  
          - **MySQL** – Stores menu items, order details, and tracks order status.  
          - **SQL Queries** – Efficient data retrieval and storage.  

        - **🌐 Web UI & Integration:**  
          - **Streamlit** – Provides an interactive web interface for chatbot interaction.  
          - **Session Management** – Stores user conversations and order history.  

        ---
        ## 🔍 **What Happens Behind the Scenes?**
        When you interact with **DineMate**, here's what happens behind the scenes:

        1️⃣ **User Input Handling:**  
        - You type a request like *"I want a Pepperoni Pizza and a Coke."*  
        - The chatbot processes it using **Qwen-2.5-32B**.

        2️⃣ **LLM Understanding & Parsing:**  
        - The AI extracts food items and quantities.  
        - Checks **menu availability** using the database.  

        3️⃣ **Order Processing & Database Update:**  
        - Adds food items to an **in-memory order session**.  
        - Calculates **total price** from the database.  
        - Updates the order in **MySQL** when confirmed.  

        4️⃣ **Order Tracking & Delivery Estimation:**  
        - When you request *"Track my order 27,"*  
        - The bot fetches the **status and estimated delivery time** from the database.  

        5️⃣ **Response Generation & UI Display:**  
        - The AI generates a **human-like response** with emojis and structured formatting.  
        - Displays the message in **Streamlit UI** in an interactive chat format.  

        ---
        ## 🔗 **Project Repository & Contributions**
        **View Source Code:** [GitHub Repository](https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot)  
        Built with ❤️ by **Muhammad Umer Khan**  

        ---
        """,
        unsafe_allow_html=True
    )

    # 📌 Footer
    # st.markdown("---")
    # st.markdown("🔗 **GitHub Repo:** [View Source Code](https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot)")
    st.markdown("© 2025 **DineMate AI** | Built with ❤️ by **Muhammad Umer Khan**")

# ✅ Run when Home is loaded
if __name__ == "__main__":
    show_home()
