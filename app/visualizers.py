"""
# DineMate Visualizers 📈

This module generates Plotly charts for analytics with enhanced styling.

Dependencies:
- plotly.express: For chart generation 📊.
- plotly.graph_objects: For advanced customizations 📉.
- logger: For structured logging 📜.
"""

import plotly.express as px
import plotly.graph_objects as go
from scripts.logger import get_logger

logger = get_logger(__name__)

# Custom color palette for vibrant, professional look
COLOR_PALETTE = ["#00C4B4", "#FF6F61", "#6B7280", "#FBBF24", "#7C3AED", "#EC4899"]

def create_monthly_revenue_chart(df):
    """📊 Generate monthly revenue trend chart with enhanced styling.

    Args:
        df: DataFrame with monthly revenue data (year, month, total_price, date).

    Returns:
        plotly.graph_objects.Figure: Line chart.
    """
    logger.info({"message": "Generating monthly revenue chart"})
    fig = px.line(
        df, x="date", y="total_price", title="📊 Monthly Revenue Trends",
        labels={"total_price": "Revenue ($)", "date": "Month"},
        markers=True, line_shape="spline", color_discrete_sequence=[COLOR_PALETTE[0]]
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis_title="Month", yaxis_title="Revenue ($)",
        xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        showlegend=False
    )
    fig.update_traces(
        line=dict(width=3), 
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="white")),
        hovertemplate="%{x|%b %Y}: $%{y:.2f}"
    )
    # Add annotation for max revenue
    max_revenue = df["total_price"].max()
    max_date = df[df["total_price"] == max_revenue]["date"].iloc[0]
    fig.add_annotation(
        x=max_date, y=max_revenue, text=f"Peak: ${max_revenue:.2f}", 
        showarrow=True, arrowhead=2, ax=20, ay=-30, font=dict(color="#FBBF24")
    )
    return fig

def create_yearly_revenue_chart(df):
    """📆 Generate yearly revenue bar chart with enhanced styling.

    Args:
        df: DataFrame with yearly revenue data (year, total_price).

    Returns:
        plotly.graph_objects.Figure: Bar chart.
    """
    logger.info({"message": "Generating yearly revenue chart"})
    fig = px.bar(
        df, x="year", y="total_price", title="📆 Yearly Revenue Breakdown",
        labels={"total_price": "Revenue ($)", "year": "Year"},
        color="total_price", color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis_title="Year", yaxis_title="Revenue ($)",
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        coloraxis_showscale=False
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:.2f}")
    return fig

def create_product_countplot(df):
    """🍽️ Generate bar chart for top-selling items with enhanced styling.

    Args:
        df: DataFrame with product counts (Product, Total Orders).

    Returns:
        plotly.graph_objects.Figure: Bar chart.
    """
    logger.info({"message": "Generating product countplot"})
    fig = px.bar(
        df, x="Product", y="Total Orders", title="🍽️ Top-Selling Items",
        labels={"Total Orders": "Orders", "Product": "Item"},
        color="Total Orders", color_continuous_scale=px.colors.sequential.Aggrnyl
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis_tickangle=-45,
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        coloraxis_showscale=False
    )
    fig.update_traces(hovertemplate="%{x}: %{y} orders")
    return fig

def create_product_pie_chart(df):
    """🥧 Generate pie chart for top 10 items with enhanced styling.

    Args:
        df: DataFrame with product counts (Product, Total Orders).

    Returns:
        plotly.graph_objects.Figure: Pie chart.
    """
    logger.info({"message": "Generating product pie chart"})
    fig = px.pie(
        df.head(10), names="Product", values="Total Orders", title="🥧 Top 10 Items",
        hole=0.4, color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(
        template="plotly_dark", 
        margin=dict(l=60, r=60, t=80, b=60), 
        paper_bgcolor="#1F2937",
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        legend=dict(font=dict(size=12, color="#FFFFFF"))
    )
    fig.update_traces(
        textinfo="percent+label", 
        hovertemplate="%{label}: %{value} orders (%{percent})",
        pull=[0.1 if i == 0 else 0 for i in range(len(df.head(10)))]  # Explode top item
    )
    return fig

def create_hourly_demand_chart(df):
    """⏳ Generate line chart for peak order hours with enhanced styling.

    Args:
        df: DataFrame with hourly order counts (Hour, Total Orders).

    Returns:
        plotly.graph_objects.Figure: Line chart.
    """
    logger.info({"message": "Generating hourly demand chart"})
    fig = px.line(
        df, x="Hour", y="Total Orders", title="⏳ Peak Ordering Hours",
        labels={"Total Orders": "Orders", "Hour": "Hour (24h)"},
        markers=True, line_shape="spline", color_discrete_sequence=[COLOR_PALETTE[1]]
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis=dict(showgrid=False, tickmode="linear", tick0=0, dtick=1, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        showlegend=False
    )
    fig.update_traces(
        line=dict(width=3), 
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="white")),
        hovertemplate="Hour %{x}: %{y} orders"
    )
    # Add annotation for peak hour
    peak_hour = df["Hour"][df["Total Orders"].idxmax()]
    peak_orders = df["Total Orders"].max()
    fig.add_annotation(
        x=peak_hour, y=peak_orders, text=f"Peak: {peak_orders} orders", 
        showarrow=True, arrowhead=2, ax=20, ay=-30, font=dict(color="#FBBF24")
    )
    return fig

def create_spending_distribution_chart(df):
    """💰 Generate histogram for customer spending with enhanced styling.

    Args:
        df: DataFrame with order data (total_price).

    Returns:
        plotly.graph_objects.Figure: Histogram.
    """
    logger.info({"message": "Generating spending distribution chart"})
    fig = px.histogram(
        df, x="total_price", nbins=20, title="💰 Customer Spending Trends",
        labels={"total_price": "Order Value ($)", "count": "Number of Orders"},
        color_discrete_sequence=[COLOR_PALETTE[2]]
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center")
    )
    fig.update_traces(hovertemplate="Order Value: $%{x:.2f}<br>Orders: %{y}")
    return fig

def create_spending_boxplot_chart(df):
    """📦 Generate box plot for order values with enhanced styling.

    Args:
        df: DataFrame with order data (total_price).

    Returns:
        plotly.graph_objects.Figure: Box plot.
    """
    logger.info({"message": "Generating spending boxplot chart"})
    fig = px.box(
        df, y="total_price", title="📦 Order Value Distribution",
        labels={"total_price": "Order Value ($)"}, color_discrete_sequence=[COLOR_PALETTE[3]]
    )
    fig.update_layout(
        template="plotly_dark", 
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center")
    )
    fig.update_traces(hovertemplate="Order Value: $%{y:.2f}")
    return fig

def create_status_pie_chart(df):
    """📊 Generate pie chart for order status distribution.

    Args:
        df: DataFrame with order status counts (status, count).

    Returns:
        plotly.graph_objects.Figure: Pie chart.
    """
    logger.info({"message": "Generating order status pie chart"})
    fig = px.pie(
        df, names="status", values="count", title="📊 Order Status Distribution",
        hole=0.4, color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(
        template="plotly_dark", 
        margin=dict(l=60, r=60, t=80, b=60), 
        paper_bgcolor="#1F2937",
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        legend=dict(font=dict(size=12, color="#FFFFFF"))
    )
    fig.update_traces(
        textinfo="percent+label", 
        hovertemplate="%{label}: %{value} orders (%{percent})",
        pull=[0.1 if status == "Canceled" else 0 for status in df["status"]]
    )
    return fig

def create_cancellation_trend_chart(df):
    """❌ Generate line chart for order cancellations over time.

    Args:
        df: DataFrame with cancellation counts by date (date, count).

    Returns:
        plotly.graph_objects.Figure: Line chart.
    """
    logger.info({"message": "Generating cancellation trend chart"})
    fig = px.line(
        df, x="date", y="count", title="❌ Order Cancellations Over Time",
        labels={"count": "Cancellations", "date": "Month"},
        markers=True, line_shape="spline", color_discrete_sequence=[COLOR_PALETTE[4]]
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis_title="Month", yaxis_title="Cancellations",
        xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        showlegend=False
    )
    fig.update_traces(
        line=dict(width=3), 
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="white")),
        hovertemplate="%{x|%b %Y}: %{y} cancellations"
    )
    # Add annotation for max cancellations
    if not df.empty:
        max_cancellations = df["count"].max()
        max_date = df[df["count"] == max_cancellations]["date"].iloc[0]
        fig.add_annotation(
            x=max_date, y=max_cancellations, text=f"Peak: {max_cancellations}", 
            showarrow=True, arrowhead=2, ax=20, ay=-30, font=dict(color="#FBBF24")
        )
    return fig

def create_aov_trend_chart(df):
    """💵 Generate line chart for average order value trends.

    Args:
        df: DataFrame with AOV data (date, avg_order_value).

    Returns:
        plotly.graph_objects.Figure: Line chart.
    """
    logger.info({"message": "Generating AOV trend chart"})
    fig = px.line(
        df, x="date", y="avg_order_value", title="💵 Average Order Value Trends",
        labels={"avg_order_value": "Average Order Value ($)", "date": "Month"},
        markers=True, line_shape="spline", color_discrete_sequence=[COLOR_PALETTE[5]]
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis_title="Month", yaxis_title="Average Order Value ($)",
        xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        showlegend=False
    )
    fig.update_traces(
        line=dict(width=3), 
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="white")),
        hovertemplate="%{x|%b %Y}: $%{y:.2f}"
    )
    # Add annotation for max AOV
    if not df.empty:
        max_aov = df["avg_order_value"].max()
        max_date = df[df["avg_order_value"] == max_aov]["date"].iloc[0]
        fig.add_annotation(
            x=max_date, y=max_aov, text=f"Peak: ${max_aov:.2f}", 
            showarrow=True, arrowhead=2, ax=20, ay=-30, font=dict(color="#FBBF24")
        )
    return fig

def create_item_revenue_chart(df):
    """💰 Generate bar chart for revenue by menu item.

    Args:
        df: DataFrame with item revenue data (Product, Total Revenue).

    Returns:
        plotly.graph_objects.Figure: Bar chart.
    """
    logger.info({"message": "Generating item revenue chart"})
    fig = px.bar(
        df, x="Product", y="Total Revenue", title="💰 Revenue by Menu Item",
        labels={"Total Revenue": "Revenue ($)", "Product": "Item"},
        color="Total Revenue", color_continuous_scale=px.colors.sequential.Turbo
    )
    fig.update_layout(
        template="plotly_dark", 
        xaxis_tickangle=-45,
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified", plot_bgcolor="#1F2937", paper_bgcolor="#1F2937",
        margin=dict(l=60, r=30, t=80, b=60),
        title=dict(font=dict(size=20, color="#FFFFFF"), x=0.5, xanchor="center"),
        coloraxis_showscale=False
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:.2f}")
    return fig