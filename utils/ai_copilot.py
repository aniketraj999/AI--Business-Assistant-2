import pandas as pd
import streamlit as st
from groq import Groq


client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


def ask_ai(question, df):

    # -----------------------------
    # Prepare data
    # -----------------------------
    data = df.copy()

    if data.empty:
        return "There is no sales data available for the selected filters."

    data["order_date"] = pd.to_datetime(
        data["order_date"],
        errors="coerce"
    )

    data = data.dropna(subset=["order_date"])

    # -----------------------------
    # Overall business metrics
    # -----------------------------
    total_revenue = data["revenue"].sum()
    total_profit = data["profit"].sum()
    total_orders = len(data)

    profit_margin = (
        (total_profit / total_revenue) * 100
        if total_revenue > 0
        else 0
    )

    # -----------------------------
    # Determine latest month
    # based on the dataset
    # -----------------------------
    latest_date = data["order_date"].max()

    latest_month_start = latest_date.replace(day=1)

    previous_month_end = (
        latest_month_start - pd.Timedelta(days=1)
    )

    previous_month_start = (
        previous_month_end.replace(day=1)
    )

    # -----------------------------
    # Last month's data
    # -----------------------------
    last_month_df = data[
        (data["order_date"] >= previous_month_start)
        &
        (data["order_date"] < latest_month_start)
    ]

    last_month_revenue = last_month_df["revenue"].sum()
    last_month_profit = last_month_df["profit"].sum()
    last_month_orders = len(last_month_df)

    last_month_margin = (
        (last_month_profit / last_month_revenue) * 100
        if last_month_revenue > 0
        else 0
    )

    # -----------------------------
    # Previous month comparison
    # -----------------------------
    two_months_ago_end = (
        previous_month_start - pd.Timedelta(days=1)
    )

    two_months_ago_start = (
        two_months_ago_end.replace(day=1)
    )

    previous_period_df = data[
        (data["order_date"] >= two_months_ago_start)
        &
        (data["order_date"] < previous_month_start)
    ]

    previous_revenue = previous_period_df["revenue"].sum()

    if previous_revenue > 0:
        revenue_growth = (
            (last_month_revenue - previous_revenue)
            / previous_revenue
        ) * 100
    else:
        revenue_growth = 0

    # -----------------------------
    # Region performance
    # -----------------------------
    region_summary = (
        last_month_df
        .groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    region_text = (
        region_summary
        .to_string()
        if not region_summary.empty
        else "No regional data available."
    )

    # -----------------------------
    # Category performance
    # -----------------------------
    category_summary = (
        last_month_df
        .groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    category_text = (
        category_summary
        .to_string()
        if not category_summary.empty
        else "No category data available."
    )

    # -----------------------------
    # Best region/category
    # -----------------------------
    if not region_summary.empty:
        best_region = region_summary.idxmax()
        best_region_revenue = region_summary.max()
    else:
        best_region = "N/A"
        best_region_revenue = 0

    if not category_summary.empty:
        best_category = category_summary.idxmax()
        best_category_revenue = category_summary.max()
    else:
        best_category = "N/A"
        best_category_revenue = 0

    # -----------------------------
    # Business summary for AI
    # -----------------------------
    summary = f"""
OVERALL BUSINESS PERFORMANCE
-----------------------------
Total Revenue: ${total_revenue:,.2f}
Total Profit: ${total_profit:,.2f}
Total Orders: {total_orders:,}
Profit Margin: {profit_margin:.2f}%

LAST MONTH PERFORMANCE
-----------------------------
Month: {previous_month_start.strftime("%B %Y")}
Revenue: ${last_month_revenue:,.2f}
Profit: ${last_month_profit:,.2f}
Orders: {last_month_orders:,}
Profit Margin: {last_month_margin:.2f}%

MONTH-OVER-MONTH
-----------------------------
Previous Month Revenue: ${previous_revenue:,.2f}
Revenue Growth: {revenue_growth:.2f}%

LAST MONTH BY REGION
-----------------------------
{region_text}

LAST MONTH BY CATEGORY
-----------------------------
{category_text}

TOP REGION LAST MONTH
-----------------------------
{best_region}
Revenue: ${best_region_revenue:,.2f}

TOP CATEGORY LAST MONTH
-----------------------------
{best_category}
Revenue: ${best_category_revenue:,.2f}
"""

    # -----------------------------
    # AI Prompt
    # -----------------------------
    prompt = f"""
You are an expert Business Intelligence Analyst.

You have access to the following REAL business data:

{summary}

User Question:
{question}

Instructions:

1. Answer the user's question directly.
2. Use the numbers from the business data above.
3. Never ask the user to provide sales figures because the data is already available.
4. If the user asks about last month, use the LAST MONTH PERFORMANCE section.
5. If the user asks about growth, use the MONTH-OVER-MONTH section.
6. If the user asks about regions, use LAST MONTH BY REGION.
7. If the user asks about categories, use LAST MONTH BY CATEGORY.
8. Give concise and practical business insights.
9. Mention exact numbers whenever possible.
10. Do not invent any data.
11. Use simple professional English.

Answer format:

Direct Answer:
[Answer the question]

Key Insight:
[Important business insight]

Recommendation:
[One practical recommendation]
"""

    # -----------------------------
    # Groq AI
    # -----------------------------
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a professional Business Intelligence Analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
