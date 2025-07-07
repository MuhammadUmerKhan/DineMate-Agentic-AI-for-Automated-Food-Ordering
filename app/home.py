"""
# DineMate Home Page 🏠

This module displays the DineMate home page, showcasing the AI-powered food ordering system's features.

Dependencies:
- streamlit: For UI rendering 📺.
- logger: For structured logging 📜.
"""

import streamlit as st, os
from scripts.logger import get_logger

logger = get_logger(__name__)

# ✅ Load centralized CSS
try:
    with open("./static/styles.css", "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

def home() -> None:
    """🏠 Display the DineMate home page."""
    logger.info({"message": "Rendering home page"})
    st.markdown(
        "<div class='header'><h1>🍽️ Welcome to DineMate</h1><p style='color: #E8ECEF;'>🚀 AI-Powered Food Ordering System</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    with st.expander("📌 About DineMate", expanded=True):
        st.markdown("""
        **DineMate** is an AI-driven platform that streamlines restaurant operations and enhances customer experience. 
        Powered by advanced AI, it offers seamless ordering, real-time tracking, and insightful analytics for restaurants. 
        Key highlights:
        - 🤖 **AI Chatbot**: Order food using natural language.
        - 🎤 **Voice Ordering**: Speak your order effortlessly.
        - 📊 **Analytics Dashboard**: Track revenue, demand, and order trends.
        - 📦 **Order Management**: Modify or cancel orders within 10 minutes.
        - 🗄️ **Optimized Database**: Fast, reliable data storage and retrieval.
        """)

    with st.expander("🛠️ Core Features", expanded=True):
        st.markdown("""
        - 🍔 **Smart Ordering**: Place orders via chatbot or voice commands.
        - 📦 **Real-Time Tracking**: Monitor order status (Pending, Preparing, Delivered, etc.).
        - 🔄 **Flexible Modifications**: Update or cancel orders within 10 minutes.
        - 🛒 **Dynamic Menu**: Admins can update items and prices easily.
        - 📊 **Business Insights**: Analyze revenue, popular items, peak hours, and cancellations.
        - 👨‍🍳 **Kitchen Efficiency**: Staff can update order statuses in real time.
        - 🎤 **Voice Interaction**: Use natural speech for ordering and tracking.
        """)

    with st.expander("🗄️ Database & Performance", expanded=True):
        st.markdown("""
        - 🗄️ **SQLite Database**: Stores 150+ orders with diverse statuses (Pending, Delivered, Canceled, etc.).
        - 📅 **Rich Data**: Orders span 2023–2025 with varied timestamps for robust analysis.
        - ⚡ **Optimized Queries**: Indexes on status and date for fast filtering and sorting.
        - 📦 **Batch Processing**: Efficient data population with batch inserts.
        - 📜 **Structured Logging**: Tracks all operations for debugging and monitoring.
        """)

    with st.expander("📊 Analytics Dashboard", expanded=True):
        st.markdown("""
        - 💰 **Revenue Trends**: Visualize monthly and yearly revenue.
        - 📋 **Order Status**: Pie charts for status distribution (e.g., Delivered, Canceled).
        - 🍽️ **Popular Items**: Bar and pie charts for top-ordered items and revenue.
        - ⏳ **Peak Hours**: Hourly demand analysis for staffing optimization.
        - 🛒 **Spending Patterns**: Histograms and boxplots for customer spending.
        - 🔍 **Filters**: Analyze by status (All, Pending, etc.) or year (2023–2025).
        - 🏆 **Actionable Insights**: Optimize menu, staffing, and promotions.
        """)

    with st.expander("🏗️ User Roles", expanded=True):
        role_data = {
            "👤 Customers": [
                "🍔 Order via chatbot or voice",
                "🔄 Modify/cancel orders within 10 minutes",
                "📦 Track order status"
            ],
            "👨‍🍳 Kitchen Staff": [
                "📦 View and update order statuses",
                "🔄 Manage non-cancelable orders"
            ],
            "📞 Customer Support": [
                "🔄 Modify or cancel orders",
                "📞 Assist customers"
            ],
            "🛡️ Admin": [
                "🛒 Manage menu items",
                "💰 Update pricing",
                "📊 Access full analytics"
            ]
        }
        for role, permissions in role_data.items():
            st.markdown(f"<h3 style='color: #DC3545;'>{role}</h3>", unsafe_allow_html=True)
            for perm in permissions:
                st.markdown(f"✔ {perm}")

    with st.expander("🚀 Getting Started", expanded=True):
        st.markdown("""
        1. 🍔 **Order**: Use the chatbot ("Order 2 burgers") or voice commands.
        2. 🔄 **Manage**: Modify or cancel orders within 10 minutes via the support panel.
        3. 📦 **Track**: Check real-time status by order ID.
        4. 📊 **Analyze**: Explore the analytics dashboard for business insights.
        """)

    with st.expander("🛠️ Technologies", expanded=True):
        tech_data = {
            "🧠 AI Chatbot": "Qwen-2.5-32B LLM for natural language ordering",
            "🎤 Voice Processing": "Whisper AI for speech-to-text and text-to-speech",
            "🛠️ Backend": "LangChain & LangGraph for workflow orchestration",
            "🗄️ Database": "SQLite with optimized schema and indexes",
            "📺 Interface": "Streamlit for responsive, interactive UI",
            "📜 Logging": "Structured logging for monitoring and debugging"
        }
        for tech, desc in tech_data.items():
            st.markdown(f"<h3 style='color: #6C757D;'>{tech}</h3>", unsafe_allow_html=True)
            st.markdown(f"✔ {desc}")

    st.markdown("""
    <h2 style='color: #343A40;'>🔗 Source Code</h2>
    <p><a href='https://github.com/MuhammadUmerKhan/DineMate-Food-Ordering-Chatbot' target='_blank' style='text-decoration: none; color: #007BFF;'>🌍 GitHub</a> - Built by Muhammad Umer Khan</p>
    """, unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>© 2025 <b>DineMate AI</b> | Powered by ❤️</p>",
        unsafe_allow_html=True
    )