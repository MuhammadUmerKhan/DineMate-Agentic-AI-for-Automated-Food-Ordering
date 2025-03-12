import pandas as pd
from collections import Counter
import json

def preprocess_data(df):
    """Process order data to extract date, month, and year."""
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    return df

def calculate_monthly_revenue(df):
    """Compute monthly revenue and format the date."""
    monthly_revenue = df.groupby(['year', 'month'])['total_price'].sum().reset_index()
    monthly_revenue['date'] = pd.to_datetime(monthly_revenue[['year', 'month']].assign(day=1))
    return monthly_revenue

def calculate_yearly_revenue(df):
    """Compute yearly revenue."""
    yearly_revenue = df.groupby("year")["total_price"].sum().reset_index()
    return yearly_revenue

def extract_product_counts(df):
    """Extracts product counts from JSON order items."""
    all_items = Counter()

    for order in df["items"]:
        try:
            # Convert string to dictionary
            order_dict = json.loads(order.replace("'", "\""))  # Ensure valid JSON format
            all_items.update(order_dict)
        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON: {order}, Error: {e}")

    # Convert to DataFrame
    product_counts = pd.DataFrame(all_items.items(), columns=["Product", "Total Orders"])
    product_counts = product_counts.sort_values(by="Total Orders", ascending=False)
    
    return product_counts

def extract_hourly_demand(df):
    """Extracts the number of orders per hour."""
    df["time"] = pd.to_datetime(df["time"], format="%I:%M:%S %p")  # Convert to datetime
    df["hour"] = df["time"].dt.hour  # Extract hour
    hourly_demand = df.groupby("hour")["id"].count().reset_index()  # Count orders per hour
    hourly_demand.columns = ["Hour", "Total Orders"]
    return hourly_demand
