import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import analyze_sales
from insights import generate_insights
from report import generate_report
from ai_summary import generate_ai_summary

st.set_page_config(
    page_title="AI Business Insights Dashboard",
    layout="wide"
)

st.title("📊 AI-Powered Business Insights Dashboard")
st.caption("Analyze sales data and generate business insights automatically")

# Sidebar
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

# Dataset loading
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

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Dataset Summary
    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Products", df["product"].nunique())
    col3.metric("Regions", df["region"].nunique())

    st.divider()

    # Analysis
    results = analyze_sales(df)

    # Key Metrics
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

    # Top region highlight
    top_region = results["region_sales"].idxmax()

    st.success(f"Top Performing Region: {top_region}")

    st.divider()

    # Sales by Region
    region_df = results["region_sales"].reset_index()
    region_df.columns = ["Region", "Sales"]

    fig1 = px.bar(
        region_df,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    # Monthly Trend
    month_df = results["monthly_sales"].reset_index()
    month_df.columns = ["Month", "Sales"]

    fig2 = px.line(
        month_df,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    # Product Performance
    st.subheader("Product Performance")

    product_sales = df.groupby("product")["sales"].sum().reset_index()

    fig3 = px.bar(
        product_sales,
        x="product",
        y="sales",
        color="product",
        title="Product Sales Comparison"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Product Distribution Pie Chart
    st.subheader("Sales Distribution by Product")

    fig4 = px.pie(
        product_sales,
        names="product",
        values="sales",
        title="Product Sales Share",
        hole=0.4
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # Insights
    st.subheader("Business Insights")

    insights = generate_insights(results)

    for insight in insights:
        st.info(insight)

    st.divider()

    # AI Business Summary 
    st.subheader("AI Business Summary")

    summary = generate_ai_summary(results)

    for s in summary:
        st.success(s)

    st.divider()

    # Download Reports
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

# Footer
st.markdown(
    """
    <hr>
    <div style="text-align:center;font-size:14px;">
        Built by Prajakta Singhal • AI Business Insights Dashboard
    </div>
    """,
    unsafe_allow_html=True
)