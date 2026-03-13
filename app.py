import streamlit as st
import pandas as pd 
import plotly.express as px
from analysis import analyze_sales
from insights import generate_insights

st.title("AI Powered Business Insights Dashboard")

uploaded_file = st.file_uploader("Upload Sales Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)
    
    results = analyze_sales(df)

    st.subheader("Key Business Metrics")

    col1, col2 = st.columns(2)

    col1.metric("Total Sales:", results["total_sales"])
    col2.metric("Best Selling Product:", results["top_product"])

    st.subheader("Sales by Region")
    
    region_df = results["region_sales"].reset_index()
    region_df.columns = ['Region', 'Sales']

    fig1 = px.bar(region_df, x = 'Region', y = 'Sales', title="Sales by Region", color='Region')

    st.plotly_chart(fig1)

    st.subheader("Monthly Sales Trend")

    month_df = results["monthly_sales"].reset_index()
    month_df.columns = ['Month', 'Sales']

    fig2 = px.line(month_df, x='Month', y='Sales', title="Monthly Sales Trend", markers=True)

    st.plotly_chart(fig2)

    st.subheader("Product Performance")
    
    product_sales = df.groupby('product')['sales'].sum().reset_index()

    fig3 = px.bar(product_sales, x='product', y='sales', title="Product Sales Comparison", color='product')

    st.plotly_chart(fig3)

    st.subheader("Business Insights")

    insights = generate_insights(results)

    for insight in insights:
        st.write(f"- {insight}")

st.markdown(
    """
    <hr>
    <div style="text-align: right; font-size: 14px;">
        Built by Prajakta Singhal
    </div>
    """,
    unsafe_allow_html=True
)

