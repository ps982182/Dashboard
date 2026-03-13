import streamlit as st
import pandas as pd 
from analysis import analyze_sales

st.title("AI Powered Business Insights Dashboard")

uploaded_file = st.file_uploader("Upload Sales Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)
    
    results = analyze_sales(df)

    st.subheader("Business Insights")

    st.write("Total Sales:", results["total_sales"])
    st.write("Best Selling Product:", results["top_product"])
