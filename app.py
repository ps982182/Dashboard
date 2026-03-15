import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import analyze_sales
from insights import generate_insights
from report import generate_report
from forecast import forecast_sales
from anomaly import detect_anomalies
from query_engine import answer_query
from ai_summary import generate_ai_summary


# Page configuration
st.set_page_config(
    page_title="AI Business Insights Dashboard",
    layout="wide"
)

# Title
st.title("📊 AI-Powered Business Insights Dashboard")
st.caption("Analyze sales data and generate business insights automatically")
st.markdown("---")


# Sidebar
st.sidebar.header("Dataset Options")

dataset_option = st.sidebar.selectbox(
    "Select Dataset",
    (
        "Upload Your Own Dataset",
        "Sample Dataset (500 rows)",
        "Sample Dataset (2000 rows)",
        "Sample Dataset (5000 rows)",
        "Enterprise Dataset (6000 rows)",
        "Enterprise Dataset (10000 rows)",
        "Enterprise Dataset (50000 rows)"
    )
)

df = None


# Dataset Loading
try:

    if dataset_option == "Upload Your Own Dataset":

        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV file",
            type=["csv"]
        )

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

    elif dataset_option == "Sample Dataset (500 rows)":
        df = pd.read_csv("data/sales_data_small_500.csv")

    elif dataset_option == "Sample Dataset (2000 rows)":
        df = pd.read_csv("data/sales_data_medium_2000.csv")

    elif dataset_option == "Sample Dataset (5000 rows)":
        df = pd.read_csv("data/sales_data_large_5000.csv")

    elif dataset_option == "Enterprise Dataset (6000 rows)":
        df = pd.read_csv("data/sales_data_6000.csv")

    elif dataset_option == "Enterprise Dataset (10000 rows)":
        df = pd.read_csv("data/sales_data_10000.csv")

    elif dataset_option == "Enterprise Dataset (50000 rows)":
        df = pd.read_csv("data/sales_data_50000.csv")

except Exception:
    st.error("Error loading dataset. Please check the file format.")


# Main Dashboard
if df is not None:

    st.success(f"Dataset loaded successfully with {len(df):,} records.")

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Dataset Summary
    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Products", df["product"].nunique())
    col3.metric("Regions", df["region"].nunique())

    st.divider()

    # Run analysis
    results = analyze_sales(df)

    # KPI Metrics
    st.subheader("Key Business Metrics")

    total_orders = len(df)
    top_region = results["region_sales"].idxmax()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${results['total_sales']:,}")
    col2.metric("Top Product", results["top_product"])
    col3.metric("Top Region", top_region)
    col4.metric("Total Orders", total_orders)

    st.divider()

    # Sales by Region
    region_df = results["region_sales"].reset_index()
    region_df.columns = ["Region", "Sales"]

    fig_region = px.bar(
        region_df.sort_values("Sales", ascending=False),
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    # Monthly Trend
    month_df = results["monthly_sales"].reset_index()
    month_df.columns = ["Month", "Sales"]

    fig_month = px.line(
        month_df,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_region, use_container_width=True)

    with col2:
        st.plotly_chart(fig_month, use_container_width=True)

    # Product Performance
    st.subheader("Product Performance")

    product_sales = df.groupby("product")["sales"].sum().reset_index()

    fig_product = px.bar(
        product_sales.sort_values("sales", ascending=False),
        x="product",
        y="sales",
        color="product",
        title="Product Sales Comparison"
    )

    st.plotly_chart(fig_product, use_container_width=True)

    # Product Distribution
    st.subheader("Sales Distribution by Product")

    fig_pie = px.pie(
        product_sales,
        names="product",
        values="sales",
        hole=0.4,
        title="Product Sales Share"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # Business Questions
    st.subheader("Business Questions")

    question = st.selectbox(
        "Select a business question",
        (
            "Which product has the highest sales?",
            "Which region has the highest sales?",
            "What are the total sales?",
            "Which month had the highest sales?",
            "Which product has the lowest sales?"
        )
    )

    if question:
        response = answer_query(df, question)
        st.info(response)

    st.divider()

    # Business Insights
    st.subheader("Business Insights")

    insights = generate_insights(results)

    for insight in insights:
        st.info(insight)

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

    st.divider()

    # AI Summary
    st.subheader("AI Business Summary")

    summary = generate_ai_summary(results)

    for s in summary:
        st.success(s)

    st.divider()

    # Sales Forecast
    st.subheader("Sales Forecast")

    try:

        forecast_df = forecast_sales(df)

        st.dataframe(forecast_df, use_container_width=True)

        fig_forecast = px.line(
            forecast_df,
            x="month",
            y="sales",
            markers=True,
            title="Predicted Sales for Upcoming Months"
        )

        fig_forecast.update_layout(
            xaxis_title="Month",
            yaxis_title="Predicted Sales"
        )

        st.plotly_chart(fig_forecast, use_container_width=True)

    except Exception:
        st.warning("Forecast could not be generated for this dataset.")

    st.divider()

    # Anomaly Detection
    st.subheader("Sales Anomaly Detection")

    try:

        anomalies = detect_anomalies(df)

        if len(anomalies) == 0:
            st.success("No unusual sales patterns detected.")

        else:
            st.warning("Unusual sales patterns detected:")
            st.dataframe(anomalies, use_container_width=True)

    except Exception:
        st.warning("Anomaly detection could not be performed.")


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