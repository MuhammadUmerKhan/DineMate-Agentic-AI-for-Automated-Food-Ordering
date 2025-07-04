import streamlit as st
import pandas as pd
from scripts.db import Database
from app.visualizers import *
from app.preprocesser import *
from streamlit_autorefresh import st_autorefresh

def show_analysis_page():
    
    # ✅ Auto-refresh every 10 seconds
    st_autorefresh(interval=10 * 1000, key="kitchen_refresh")  # 🔄 Refresh every 10 seconds
    """📊 Enhanced Business Analysis Dashboard"""
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>💹 Business Performance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px;'>Gain deep insights into your restaurant's performance with <b>real-time revenue analysis, most demanded products, and customer spending trends</b>.</p>", unsafe_allow_html=True)

    # ✅ Fetch Data from the Database
    db = Database()
    df = db.fetch_order_data()
    if df.empty:
        st.warning("⚠ No data available for analysis.")
        return

    # ✅ Preprocess Data
    preprocessed_data = preprocess_data(df)

    with st.expander("💰 Revenue Trends", expanded=True):
    # 🎯 **Revenue Analysis Section**

        st.markdown("### 📆 Monthly Revenue Analysis")
        monthly_revenue = calculate_monthly_revenue(preprocessed_data)
        fig_monthly = create_monthly_revenue_chart(monthly_revenue)
        st.plotly_chart(fig_monthly, use_container_width=True)

        st.markdown("### 📅 Yearly Revenue Analysis")
        yearly_revenue = calculate_yearly_revenue(preprocessed_data)
        fig_yearly = create_yearly_revenue_chart(yearly_revenue)
        st.plotly_chart(fig_yearly, use_container_width=True)

    st.divider()
    
    # 📌 **Most Demanded Products**
    with st.expander("🍽️ Most Popular Food Items", expanded=True):
        st.markdown("### 📊 Top Ordered Products")
        product_counts = extract_product_counts(preprocessed_data)
        fig_countplot = create_product_countplot(product_counts)
        fig_pie_chart = create_product_pie_chart(product_counts)
        
        st.plotly_chart(fig_countplot, use_container_width=True)
        st.plotly_chart(fig_pie_chart, use_container_width=True)
    
    st.divider()
    
    # ⏳ **Peak Order Hours**
    with st.expander("⏳ Peak Customer Ordering Hours", expanded=True):
        st.markdown("### 🕒 When Do Customers Order the Most?")
        hourly_demand = extract_hourly_demand(preprocessed_data)
        fig_hourly = create_hourly_demand_chart(hourly_demand)
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    st.divider()
    
    # 💰 **Customer Spending Trends**
    with st.expander("💰 Customer Spending Patterns", expanded=True):
        st.markdown("### 🛒 How Much Are Customers Spending?")
        fig_histogram = create_spending_distribution_chart(preprocessed_data)
        fig_boxplot = create_spending_boxplot_chart(preprocessed_data)
        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(fig_histogram, use_container_width=True)
        with col6:
            st.plotly_chart(fig_boxplot, use_container_width=True)
    
    st.divider()
    st.markdown("""
    **📌 Key Insights:**
    - 🏆 Identify your **bestselling food items** and **optimize your menu**.
    - ⏳ Recognize **peak order hours** to **streamline kitchen operations**.
    - 💰 Analyze **spending behavior** and create **promotions for high-value customers**.
    """)