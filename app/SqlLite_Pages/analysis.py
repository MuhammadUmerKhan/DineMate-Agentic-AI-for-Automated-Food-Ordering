import streamlit as st
import pandas as pd
import plotly.express as px
from database.SQLLITE_db import Database
from app.SqlLite_Pages.visualizers import *
from app.SqlLite_Pages.preprocesser import *

def show_analysis_page():
    """📊 Analysis Dashboard"""

    # 🎨 **Main Dashboard Title**
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>📈 Business Insights Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px;'>Gain insights into revenue, demand patterns, and customer behavior.</p>", unsafe_allow_html=True)
    st.divider()

    # ✅ **Fetch Data**
    db = Database()
    df = db.fetch_order_data()

    if df.empty:
        st.warning("⚠ No data available for analysis.")
        return

    # ✅ **Preprocess Data**
    preprocessed_data = preprocess_data(df)

    # 🎯 **Revenue Analysis (Monthly & Yearly Side by Side)**
    st.markdown("## 💰 Revenue Analysis")
    st.write("Analyze revenue trends across different time periods.")

    # 🎯 **Dropdown for Monthly Analysis Type**
    month_analysis = st.selectbox(
        "📊 Select Monthly Analysis Type:",
        ["📆 Monthly for All Years", "📅 Monthly for a Specific Year"]
    )

    if month_analysis == "📆 Monthly for All Years":
        monthly_revenue = calculate_monthly_revenue(preprocessed_data)
        fig_monthly = create_monthly_revenue_chart(monthly_revenue)
        st.plotly_chart(fig_monthly, use_container_width=True)

    elif month_analysis == "📅 Monthly for a Specific Year":
        # ✅ **Extract Available Years from Data**
        available_years = sorted(preprocessed_data["year"].unique())

        # 🎯 **Slider for Year Selection**
        selected_year = st.slider(
            "📅 Select Year:",
            min_value=min(available_years),
            max_value=max(available_years),
            value=min(available_years)
        )

        # ✅ **Filter Data for Selected Year**
        filtered_data = preprocessed_data[preprocessed_data["year"] == selected_year]
        monthly_revenue = calculate_monthly_revenue(filtered_data)

        fig_monthly_filtered = create_monthly_revenue_chart(monthly_revenue)
        st.plotly_chart(fig_monthly_filtered, use_container_width=True)

    yearly_revenue = calculate_yearly_revenue(preprocessed_data)
    fig_yearly = create_yearly_revenue_chart(yearly_revenue)
    st.plotly_chart(fig_yearly, use_container_width=True)

    st.divider()

    # 🎯 **Most Demanded Products**
    st.subheader("🍽️ Most Ordered Menu Items")

    product_counts = extract_product_counts(preprocessed_data)
    fig_countplot = create_product_countplot(product_counts)
    st.plotly_chart(fig_countplot, use_container_width=True)

    fig_pie_chart = create_product_pie_chart(product_counts)
    st.plotly_chart(fig_pie_chart, use_container_width=True)

    st.divider()

    # ✅ Extract hourly demand
    hourly_demand = extract_hourly_demand(preprocessed_data)
    # 🎯 **Peak Order Hours**
    st.subheader("⏳ Order Timing Insights")

    fig_hourly = create_hourly_demand_chart(hourly_demand)

    if fig_hourly:
        st.plotly_chart(fig_hourly, use_container_width=True)
    else:
        st.warning("⚠ No orders were placed on the selected date.")

    st.divider()

    # 🎯 **Customer Spending Analysis**
    st.subheader("💰 Customer Spending Behavior")

    fig_histogram = create_spending_distribution_chart(preprocessed_data)
    st.plotly_chart(fig_histogram, use_container_width=True)

    fig_boxplot = create_spending_boxplot_chart(preprocessed_data)
    st.plotly_chart(fig_boxplot, use_container_width=True)

    st.divider()

    st.markdown(
        """
        <div style='text-align: center; padding: 10px; margin-top: 20px;'>
            <h5 style='color: #FFA500;'>🍽️ Data-Driven Decisions, Smarter Business!</h5>
            <p style='font-size: 16px; color: #DDDDDD;'>🎯 Empowering restaurants with data-driven decisions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
