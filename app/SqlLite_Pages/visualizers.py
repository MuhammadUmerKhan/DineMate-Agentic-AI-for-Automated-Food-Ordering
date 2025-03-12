import plotly.express as px

def create_monthly_revenue_chart(df):
    """📊 Generates a well-defined monthly revenue trend chart with improved dark theme aesthetics."""
    fig = px.line(
        df, 
        x="date", 
        y="total_price", 
        title="📊 Monthly Revenue Analysis: Trends & Patterns",
        labels={"total_price": "Revenue ($)", "date": "Month"},
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#00C3FF"]
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=60, r=30, t=60, b=60),
    )

    fig.update_traces(
        hoverinfo="text+name",
        line=dict(width=3),
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="white"))
    )

    return fig


def create_yearly_revenue_chart(df):
    """📆 Generates an intuitive yearly revenue bar chart with enhanced readability."""
    fig = px.bar(
        df,
        x="year",
        y="total_price",
        title="📆 Yearly Revenue Breakdown",
        labels={"total_price": "Total Revenue ($)", "year": "Year"},
        color="total_price",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Total Revenue ($)",
        xaxis=dict(showgrid=False, tickangle=0, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=60, r=30, t=60, b=60),
    )

    return fig


def create_product_countplot(df):
    """🍽️ Generates a bar chart for most demanded products with enhanced visuals."""
    fig = px.bar(
        df,
        x="Product",
        y="Total Orders",
        title="🍽️ Top-Selling Menu Items",
        labels={"Total Orders": "Orders Count", "Product": "Menu Item"},
        color="Total Orders",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_tickangle=-45,
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=60, r=30, t=60, b=60)
    )
    return fig


def create_product_pie_chart(df):
    """🥧 Generates a sleek pie chart for top 10 most demanded products."""
    fig = px.pie(
        df.head(10),
        names="Product",
        values="Total Orders",
        title="🥧 Top 10 Best-Selling Menu Items",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=60, r=60, t=60, b=60),
        paper_bgcolor="#0E1117"
    )
    
    return fig


def create_hourly_demand_chart(df):
    """⏳ Generates a line chart for peak order hours with better visualization."""
    fig = px.line(
        df,
        x="Hour",
        y="Total Orders",
        title="⏳ Peak Ordering Hours: When Customers Order the Most",
        labels={"Total Orders": "Orders Count", "Hour": "Hour of the Day (24h format)"},
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#FFA500"]
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(showgrid=False, tickmode="linear", tick0=0, dtick=1, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=60, r=30, t=60, b=60)
    )

    return fig


def create_spending_distribution_chart(df):
    """💰 Generates a well-defined histogram for customer spending behavior."""
    fig = px.histogram(
        df,
        x="total_price",
        nbins=20,
        title="💰 Customer Spending Trends: How Much They Spend",
        labels={"total_price": "Order Value ($)"},
        color_discrete_sequence=["#760451"]
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(showgrid=False, tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=60, r=30, t=60, b=60)
    )

    return fig


def create_spending_boxplot_chart(df):
    """📦 Generates a box plot for customer spending patterns to detect outliers."""
    fig = px.box(
        df,
        y="total_price",
        title="📦 Customer Order Value Distribution (Box Plot)",
        labels={"total_price": "Order Value ($)"},
        color_discrete_sequence=["#FF4500"]
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=14, color="#FFFFFF")),
        hovermode="x unified",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=60, r=30, t=60, b=60)
    )

    return fig
