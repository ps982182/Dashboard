import pandas as pd

def analyze_sales(df):

    # total sales 
    total_sales = df['sales'].sum()

    # best selling product 
    top_product = df.groupby('product')['sales'].sum().idxmax()

    # sales by region 
    region_sales = df.groupby('region')['sales'].sum()

    # monthly sales trend 
    monthly_sales = df.groupby('month')["sales"].sum()

    return {
        "total_sales": total_sales,
        "top_product": top_product,
        "region_sales": region_sales,
        "monthly_sales": monthly_sales
    }