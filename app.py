import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import analyze_sales
from insights import generate_insights
from report import generate_report

st.set_page_config(
    page_title="AI Business Insights Dashboard",
    layout="wide"
)

st.title("📊 AI-Powered Business Insights Dashboard")
st.caption("Analyze sales data and generate business insights automatically")

# Sidebar dataset selector
st.sidebar.header("Dataset Options")

dataset_option = st.sidebar.selectbox(
    "Select Dataset",
    (
        "Upload Your Own Dataset",
        "Sample Dataset (Small)",
        "Sample Dataset (Medium)",
        "Sample Dataset (Large)"
    )
)

df = None

if dataset_option == "Upload Your Own Dataset":

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file", type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

elif dataset_option == "Sample Dataset (Small)":
    df = pd.read_csv("data/sales_data_small.csv")

elif dataset_option == "Sample Dataset (Medium)":
    df = pd.read_csv("data/sales_data_medium.csv")

elif dataset_option == "Sample Dataset (Large)":
    df = pd.read_csv("data/sales_data_large.csv")


if df is not None:

    st.subheader("Dataset Preview")
    st.dataframe(df)

    results = analyze_sales(df)

    st.divider()

    st.subheader("Key Business Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Sales",
        f"${results['total_sales']:,}"
    )

    col2.metric(
        "Best Selling Product",
        results["top_product"]
    )

    st.divider()

    region_df = results["region_sales"].reset_index()
    region_df.columns = ["Region", "Sales"]

    fig1 = px.bar(
        region_df,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    month_df = results["monthly_sales"].reset_index()
    month_df.columns = ["Month", "Sales"]

    fig2 = px.line(
        month_df,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    product_sales = df.groupby("product")["sales"].sum().reset_index()

    fig3 = px.bar(
        product_sales,
        x="product",
        y="sales",
        color="product",
        title="Product Sales Comparison"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    st.subheader("Business Insights")

    insights = generate_insights(results)

    for insight in insights:
        st.info(insight)

    st.divider()

    st.subheader("Download Reports")

    metrics_df, insights_df = generate_report(results, insights)

    st.download_button(
        "Download Sales Metrics",
        metrics_df.to_csv(index=False),
        "sales_metrics_report.csv",
        "text/csv"
    )

    st.download_button(
        "Download Business Insights",
        insights_df.to_csv(index=False),
        "business_insights_report.csv",
        "text/csv"
    )
