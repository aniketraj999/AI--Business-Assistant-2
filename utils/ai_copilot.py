from groq import Groq
import streamlit as st


def ask_ai(question, df):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "❌ GROQ_API_KEY not found. Please add it to your Streamlit secrets."

        client = Groq(api_key=api_key)

        summary = f"""
Total Revenue: {df['revenue'].sum():,.2f}
Total Profit: {df['profit'].sum():,.2f}
Orders: {len(df)}
Regions: {', '.join(df['region'].astype(str).unique())}
Categories: {', '.join(df['category'].astype(str).unique())}
"""

        prompt = f"""
You are an expert Business Intelligence Analyst.

Business Summary:
{summary}

User Question:
{question}

Answer professionally in simple English with insights.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AI Error: {str(e)}"
