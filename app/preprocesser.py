"""
# DineMate Data Preprocessor 🛠️

This module preprocesses order data for analytics.

Dependencies:
- pandas: For data processing 📊.
- json: For JSON handling 🗃️.
- logger: For structured logging 📜.
"""

import pandas as pd, json
from collections import Counter
from scripts.logger import get_logger
from scripts.config import STATIC
import streamlit as st

logger = get_logger(__name__)

# ✅ Load centralized CSS
try:
    with open(STATIC, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    logger.error({"message": "styles.css not found"})
    st.error("⚠ CSS file not found. Please ensure static/styles.css exists.")

@st.cache_data(ttl=60)
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info({"rows": len(df), "message": "Preprocessing data"})
    try:
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.month_name()
        return df
    except Exception as e:
        logger.error({"error": str(e), "message": "Failed to preprocess data"})
        return df

@st.cache_data(ttl=60)
def calculate_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    logger.info({"message": "Calculating monthly revenue"})
    monthly_revenue = df.groupby(['year', 'month'])['total_price'].sum().reset_index()
    monthly_revenue['date'] = pd.to_datetime(monthly_revenue[['year', 'month']].assign(day=1))
    return monthly_revenue

@st.cache_data(ttl=60)
def calculate_yearly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    logger.info({"message": "Calculating yearly revenue"})
    return df.groupby("year")["total_price"].sum().reset_index()

@st.cache_data(ttl=60)
def extract_product_counts(df: pd.DataFrame) -> pd.DataFrame:
    logger.info({"message": "Extracting product counts"})
    all_items = Counter()
    for order in df["items"]:
        try:
            order_dict = json.loads(order.replace("'", "\""))
            all_items.update(order_dict)
        except json.JSONDecodeError as e:
            logger.warning({"error": str(e), "order": order})
    product_counts = pd.DataFrame(all_items.items(), columns=["Product", "Total Orders"])
    product_counts = product_counts.sort_values(by="Total Orders", ascending=False)
    return product_counts

@st.cache_data(ttl=60)
def extract_hourly_demand(df: pd.DataFrame) -> pd.DataFrame:
    logger.info({"message": "Extracting hourly demand"})
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"], format="%I:%M:%S %p")
    df["hour"] = df["time"].dt.hour
    hourly_demand = df.groupby("hour")["id"].count().reset_index()
    hourly_demand.columns = ["Hour", "Total Orders"]
    return hourly_demand