def generate_insights(results):

    insights = []

    insights.append(
        f"{results['top_product']} is the best selling product."
    )

    top_region = results["region_sales"].idxmax()

    insights.append(
        f"{top_region} region generates the highest revenue."
    )

    monthly_sales = results["monthly_sales"]

    if monthly_sales.iloc[-1] > monthly_sales.iloc[0]:

        insights.append(
            "Sales show an overall increasing trend across months."
        )

    else:

        insights.append(
            "Sales fluctuate across months without a clear upward trend."
        )

    return insights