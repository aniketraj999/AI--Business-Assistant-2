# ==============================
# Enterprise AI Business Assistant
# app.py (Part 1)
# ==============================

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from sklearn.linear_model import LinearRegression

from utils.database import load_data
from utils.ai_copilot import ask_ai


# ------------------------------------
# PAGE CONFIG
# ------------------------------------
st.set_page_config(
    page_title="Enterprise AI Business Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------
# LOAD CSS
# ------------------------------------
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass


load_css()


# ------------------------------------
# LOAD DATA
# ------------------------------------
@st.cache_data
def get_data():
    return load_data()


df = get_data()


# ------------------------------------
# SIDEBAR
# ------------------------------------
st.sidebar.title("📊 Enterprise BI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Copilot",
        "Forecast",
        "Reports"
    ]
)


# ------------------------------------
# FILTERS
# ------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

regions = sorted(df["region"].dropna().unique())
categories = sorted(df["category"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

start_date = st.sidebar.date_input(
    "Start Date",
    value=df["order_date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    value=df["order_date"].max()
)

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["region"].isin(selected_regions)
]

filtered_df = filtered_df[
    filtered_df["category"].isin(selected_categories)
]

filtered_df = filtered_df[
    (filtered_df["order_date"] >= pd.to_datetime(start_date))
    &
    (filtered_df["order_date"] <= pd.to_datetime(end_date))
]
# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("📊 Enterprise AI Business Assistant")
    st.caption("AI Powered Business Intelligence Dashboard")

    # -----------------------------------
    # KPI CALCULATIONS
    # -----------------------------------

    total_revenue = filtered_df["revenue"].sum()
    total_profit = filtered_df["profit"].sum()
    total_orders = len(filtered_df)

    profit_margin = (
        (total_profit / total_revenue) * 100
        if total_revenue > 0 else 0
    )

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0 else 0
    )

    # -----------------------------------
    # BUSINESS HEALTH SCORE
    # -----------------------------------

    score = 40

    if profit_margin >= 30:
        score += 30
    elif profit_margin >= 20:
        score += 20
    elif profit_margin >= 10:
        score += 10

    if total_orders > 100:
        score += 15

    if total_profit > 0:
        score += 15

    score = min(score, 100)

    # -----------------------------------
    # EXECUTIVE OVERVIEW
    # -----------------------------------

    st.markdown("## 📌 Executive Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

    c2.metric(
        "📈 Profit",
        f"${total_profit:,.0f}"
    )

    c3.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

    c4.metric(
        "📊 Margin",
        f"{profit_margin:.2f}%"
    )

    c5.metric(
        "🧾 Avg Order",
        f"${avg_order_value:,.2f}"
    )

    st.divider()

    # -----------------------------------
    # BUSINESS HEALTH
    # -----------------------------------

    health1, health2 = st.columns([3, 1])

    with health1:

        st.subheader("🏥 Business Health")

        st.progress(score / 100)

        st.metric(
            "Overall Score",
            f"{score}/100"
        )

    with health2:

        if score >= 90:
            st.success("Excellent")

        elif score >= 75:
            st.success("Healthy")

        elif score >= 60:
            st.warning("Average")

        else:
            st.error("Needs Attention")

    st.divider()

    # -----------------------------------
    # REVENUE TREND
    # -----------------------------------

    trend = (
        filtered_df
        .groupby("order_date", as_index=False)["revenue"]
        .sum()
    )

    fig_trend = px.line(
        trend,
        x="order_date",
        y="revenue",
        title="Revenue Trend",
        markers=True
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    # -----------------------------------
    # REGION + CATEGORY
    # -----------------------------------

    left, right = st.columns(2)

    with left:

        region_df = (
            filtered_df
            .groupby("region", as_index=False)["revenue"]
            .sum()
        )

        fig_region = px.bar(
            region_df,
            x="region",
            y="revenue",
            color="region",
            title="Revenue by Region"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    with right:

        category_df = (
            filtered_df
            .groupby("category", as_index=False)["profit"]
            .sum()
        )

        fig_category = px.pie(
            category_df,
            names="category",
            values="profit",
            title="Profit by Category"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )
    # -----------------------------------
    # TOP 10 PRODUCTS
    # -----------------------------------

    st.divider()
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df
        .groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="revenue",
        y="product",
        orientation="h",
        color="revenue",
        title="Top Products by Revenue"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    # -----------------------------------
    # TOP CUSTOMERS
    # -----------------------------------

    st.subheader("👑 Top 10 Customers")

    top_customers = (
        filtered_df
        .groupby("customer_name", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    fig_customers = px.bar(
        top_customers,
        x="customer_name",
        y="revenue",
        color="revenue",
        title="Top Customers"
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )

    # -----------------------------------
    # MONTHLY REVENUE
    # -----------------------------------

    st.subheader("📅 Monthly Revenue")

    monthly_df = filtered_df.copy()

    monthly_df["Month"] = (
        monthly_df["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        monthly_df
        .groupby("Month", as_index=False)["revenue"]
        .sum()
    )

    fig_month = px.line(
        monthly_sales,
        x="Month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

    # -----------------------------------
    # SALESPERSON PERFORMANCE
    # -----------------------------------

    st.subheader("👨‍💼 Salesperson Performance")

    sales_df = (
        filtered_df
        .groupby("salesperson", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    fig_sales = px.bar(
        sales_df,
        x="salesperson",
        y="revenue",
        color="revenue",
        title="Salesperson Performance"
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )

    # -----------------------------------
    # CORRELATION HEATMAP
    # -----------------------------------

    st.subheader("🔥 Correlation Heatmap")

    corr = filtered_df[
        [
            "quantity",
            "unit_price",
            "cost",
            "revenue",
            "profit"
        ]
    ].corr()

    fig_heat = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Correlation Matrix"
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

    # -----------------------------------
    # AI BUSINESS INSIGHTS
    # -----------------------------------

    st.divider()
    st.subheader("💡 AI Business Insights")

    best_region = (
        filtered_df
        .groupby("region")["revenue"]
        .sum()
        .idxmax()
    )

    best_category = (
        filtered_df
        .groupby("category")["profit"]
        .sum()
        .idxmax()
    )

    best_customer = (
        filtered_df
        .groupby("customer_name")["revenue"]
        .sum()
        .idxmax()
    )

    col1, col2, col3 = st.columns(3)

    col1.success(f"🌍 Best Region\n\n**{best_region}**")
    col2.success(f"📦 Best Category\n\n**{best_category}**")
    col3.success(f"👑 Top Customer\n\n**{best_customer}**")
# ==========================================
# FORECAST PAGE
# ==========================================

elif page == "Forecast":

    st.title("📈 Revenue Forecast")

    forecast_df = (
        filtered_df
        .groupby("order_date", as_index=False)["revenue"]
        .sum()
        .sort_values("order_date")
    )

    forecast_df["Day"] = np.arange(len(forecast_df))

    X = forecast_df[["Day"]]
    y = forecast_df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(
        len(forecast_df),
        len(forecast_df) + 30
    ).reshape(-1, 1)

    future_pred = model.predict(future_days)

    future_dates = pd.date_range(
        forecast_df["order_date"].max() + pd.Timedelta(days=1),
        periods=30
    )

    future = pd.DataFrame({
        "order_date": future_dates,
        "revenue": future_pred
    })

    fig = px.line(
        forecast_df,
        x="order_date",
        y="revenue",
        title="30-Day Revenue Forecast"
    )

    fig.add_scatter(
        x=future["order_date"],
        y=future["revenue"],
        mode="lines",
        name="Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Predicted Average Revenue",
        f"${future['revenue'].mean():,.2f}"
    )


# ==========================================
# AI COPILOT
# ==========================================

elif page == "AI Copilot":

    st.title("🤖 AI Business Copilot")

    question = st.text_area(
        "Ask anything about your business",
        placeholder="Example: Which region generated the highest revenue?"
    )

    if st.button("🚀 Ask AI", use_container_width=True):

        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI is thinking..."):

                try:
                    answer = ask_ai(question, filtered_df)
                    st.success(answer)

                except Exception as e:
                    st.error(f"AI Error: {e}")


# ==========================================
# REPORTS
# ==========================================

elif page == "Reports":

    st.title("📄 Business Reports")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV Report",
        csv,
        file_name="business_report.csv",
        mime="text/csv"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue",
        f"${filtered_df['revenue'].sum():,.0f}"
    )

    col2.metric(
        "Profit",
        f"${filtered_df['profit'].sum():,.0f}"
    )

    col3.metric(
        "Orders",
        len(filtered_df)
    )