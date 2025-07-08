"""
# DineMate Analysis Dashboard 🧮

This module provides a comprehensive business analytics dashboard for DineMate.

Dependencies:
- streamlit: For UI rendering 📺.
- pandas: For data processing 📊.
- db: For database operations 🗄️.
- visualizers: For Plotly charts 📈.
- preprocesser: For data preprocessing 🛠️.
- logger: For structured logging 📜.
"""

import streamlit as st
import pandas as pd
import json
from typing import Optional
from scripts.db import Database
from app.visualizers import (
    create_monthly_revenue_chart,
    create_yearly_revenue_chart,
    create_product_countplot,
    create_product_pie_chart,
    create_hourly_demand_chart,
    create_spending_distribution_chart,
    create_spending_boxplot_chart,
    create_status_pie_chart,
    create_cancellation_trend_chart,
    create_aov_trend_chart,
    create_item_revenue_chart,
)
from app.preprocesser import preprocess_data
from scripts.logger import get_logger
from scripts.config import STATIC_CSS_PATH
from streamlit_autorefresh import st_autorefresh

logger = get_logger(__name__)

# ✅ Load centralized CSS
try:
    with open(STATIC_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

@st.cache_data(ttl=60)
def fetch_and_preprocess_data(status: Optional[str] = "Delivered") -> Optional[pd.DataFrame]:
    try:
        db = Database()
        df = db.fetch_order_data(status)
        if df.empty:
            logger.warning({"status": status, "message": "No data available for analysis"})
            return None
        preprocessed_data = preprocess_data(df)
        logger.info({"status": status, "rows": len(df), "message": "Data fetched and preprocessed"})
        return preprocessed_data
    except Exception as e:
        logger.error({"error": str(e), "status": status, "message": "Failed to fetch/preprocess data"})
        return None
    finally:
        db.close_connection()

def show_analysis_page() -> None:
    st_autorefresh(interval=10_000, key="analysis_refresh")

    st.markdown(
        "<div class='header'><h1>📶 Analytics Dashboard</h1><p style='color: #E8ECEF;'>📊 Insights on revenue, orders, and more</p></div>",
        unsafe_allow_html=True
    )
    st.divider()

    # Sidebar for filters
    st.sidebar.markdown("<h3 style='color: #E8ECEF;'>🛠️ Dashboard Filters</h3>", unsafe_allow_html=True)
    status_options = ["All", "Pending", "Preparing", "In Process", "Ready", "Completed", "Delivered", "Canceled"]
    status_filter = st.sidebar.selectbox("Order Status", status_options, help="Filter orders by status")
    year_filter = st.sidebar.multiselect(
        "Select Years", options=[2023, 2024, 2025], default=[2025], help="Filter data by year"
    )

    with st.spinner("⏳ Loading analytics data..."):
        preprocessed_data = fetch_and_preprocess_data(status_filter)
        if preprocessed_data is None:
            st.markdown(
                "<div class='warning-container'><h3 style='color: #EF0606;'>⚠ No Data</h3><p>No data available for analysis.</p></div>",
                unsafe_allow_html=True
            )
            return

        if year_filter:
            preprocessed_data = preprocessed_data[preprocessed_data["year"].isin(year_filter)]
            if preprocessed_data.empty:
                st.markdown(
                    "<div class='warning-container'><h3 style='color: #EF0606;'>⚠ No Data</h3><p>No data available for selected years.</p></div>",
                    unsafe_allow_html=True
                )
                return

    # Summary Metrics
    st.markdown("<h2 style='color: #E8ECEF;'>📊 Key Metrics</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_revenue = preprocessed_data["total_price"].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        total_orders = len(preprocessed_data)
        st.metric("Total Orders", f"{total_orders:,}")
    with col3:
        if status_filter == "All":
            cancellation_rate = (preprocessed_data["status"] == "Canceled").mean() * 100
            st.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")
        else:
            st.metric("Cancellation Rate", "N/A (Filtered by status)")
    with col4:
        avg_order_value = preprocessed_data["total_price"].mean()
        st.metric("Avg Order Value", f"${avg_order_value:.2f}")

    st.divider()

    # Revenue Trends
    with st.expander("💰 Revenue Trends", expanded=True):
        st.markdown("### 📆 Revenue Over Time")
        col1, col2 = st.columns(2)
        with col1:
            with st.spinner("📈 Generating monthly revenue chart..."):
                monthly_revenue = preprocessed_data.groupby(['year', 'month'])['total_price'].sum().reset_index()
                monthly_revenue['date'] = pd.to_datetime(monthly_revenue[['year', 'month']].assign(day=1))
                fig_monthly = create_monthly_revenue_chart(monthly_revenue)
                st.plotly_chart(fig_monthly, use_container_width=True)
        with col2:
            with st.spinner("📈 Generating yearly revenue chart..."):
                yearly_revenue = preprocessed_data.groupby("year")["total_price"].sum().reset_index()
                fig_yearly = create_yearly_revenue_chart(yearly_revenue)
                st.plotly_chart(fig_yearly, use_container_width=True)

    st.divider()

    # Order Status Analysis
    if status_filter == "All":
        with st.expander("📊 Order Status Analysis", expanded=True):
            st.markdown("### 📋 Order Status Breakdown")
            with st.spinner("📈 Generating status pie chart..."):
                status_counts = preprocessed_data["status"].value_counts().reset_index()
                status_counts.columns = ["status", "count"]
                fig_status = create_status_pie_chart(status_counts)
                st.plotly_chart(fig_status, use_container_width=True)

            st.markdown("### ❌ Cancellations Over Time")
            with st.spinner("📈 Generating cancellation trend chart..."):
                cancellations = preprocessed_data[preprocessed_data["status"] == "Canceled"]
                cancellation_trends = cancellations.groupby(['year', 'month'])["id"].count().reset_index()
                cancellation_trends['date'] = pd.to_datetime(cancellation_trends[['year', 'month']].assign(day=1))
                cancellation_trends = cancellation_trends.rename(columns={"id": "count"})
                fig_cancellations = create_cancellation_trend_chart(cancellation_trends)
                st.plotly_chart(fig_cancellations, use_container_width=True)

    st.divider()

    # Popular Items
    with st.expander("🍽️ Popular Items", expanded=True):
        st.markdown("### 📊 Top Ordered Products")
        col1, col2 = st.columns(2)
        with col1:
            with st.spinner("📈 Generating product charts..."):
                product_counts = preprocessed_data['items'].apply(lambda x: pd.Series(json.loads(x.replace("'", "\"")))).sum().reset_index()
                product_counts.columns = ["Product", "Total Orders"]
                product_counts = product_counts.sort_values(by="Total Orders", ascending=False)
                fig_countplot = create_product_countplot(product_counts)
                st.plotly_chart(fig_countplot, use_container_width=True)
        with col2:
            with st.spinner("📈 Generating product pie chart..."):
                fig_pie_chart = create_product_pie_chart(product_counts)
                st.plotly_chart(fig_pie_chart, use_container_width=True)

        st.markdown("### 💰 Revenue by Menu Item")
        with st.spinner("📈 Generating item revenue chart..."):
            menu = Database().load_menu()
            menu_dict = {item["name"].lower(): float(item["price"]) for item in menu} if menu else {}
            item_revenue = preprocessed_data['items'].apply(lambda x: pd.Series(json.loads(x.replace("'", "\"")))).sum().reset_index()
            item_revenue.columns = ["Product", "Quantity"]
            item_revenue["Total Revenue"] = item_revenue.apply(
                lambda row: row["Quantity"] * menu_dict.get(row["Product"].lower(), 0), axis=1
            )
            item_revenue = item_revenue.sort_values(by="Total Revenue", ascending=False)
            fig_item_revenue = create_item_revenue_chart(item_revenue)
            st.plotly_chart(fig_item_revenue, use_container_width=True)

    st.divider()

    # Peak Hours
    with st.expander("⏳ Peak Ordering Hours", expanded=True):
        st.markdown("### 🕒 When Do Customers Order Most?")
        with st.spinner("📈 Generating hourly demand chart..."):
            hourly_demand = preprocessed_data.copy()
            hourly_demand["time"] = pd.to_datetime(hourly_demand["time"], format="%I:%M:%S %p")
            hourly_demand["hour"] = hourly_demand["time"].dt.hour
            hourly_demand = hourly_demand.groupby("hour")["id"].count().reset_index()
            hourly_demand.columns = ["Hour", "Total Orders"]
            fig_hourly = create_hourly_demand_chart(hourly_demand)
            st.plotly_chart(fig_hourly, use_container_width=True)

    st.divider()

    # Spending Patterns
    with st.expander("💰 Customer Spending Patterns", expanded=True):
        st.markdown("### 🛒 How Much Are Customers Spending?")
        col1, col2 = st.columns(2)
        with col1:
            with st.spinner("📈 Generating spending histogram..."):
                fig_histogram = create_spending_distribution_chart(preprocessed_data)
                st.plotly_chart(fig_histogram, use_container_width=True)
        with col2:
            with st.spinner("📈 Generating spending boxplot..."):
                fig_boxplot = create_spending_boxplot_chart(preprocessed_data)
                st.plotly_chart(fig_boxplot, use_container_width=True)

        st.markdown("### 💵 Average Order Value Trends")
        with st.spinner("📈 Generating AOV trend chart..."):
            aov_data = preprocessed_data.groupby(['year', 'month'])["total_price"].mean().reset_index()
            aov_data['date'] = pd.to_datetime(aov_data[['year', 'month']].assign(day=1))
            aov_data = aov_data.rename(columns={"total_price": "avg_order_value"})
            fig_aov = create_aov_trend_chart(aov_data)
            st.plotly_chart(fig_aov, use_container_width=True)

    st.divider()
    st.markdown(
        """
        **📌 Actionable Insights:**
        - 🏆 **Optimize Menu**: Promote high-revenue and top-selling items.
        - ⏳ **Staff Scheduling**: Increase staff during peak hours.
        - 💰 **Targeted Promotions**: Offer discounts to boost AOV during low-spending periods.
        - ❌ **Reduce Cancellations**: Investigate cancellation spikes to improve operations.
        """, 
        unsafe_allow_html=True
    )