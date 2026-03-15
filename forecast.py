from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def forecast_sales(df):

    monthly = df.groupby("month")["sales"].sum().reset_index()

    # Convert month column to datetime if needed
    monthly["month"] = pd.to_datetime(monthly["month"])

    X = np.arange(len(monthly)).reshape(-1,1)
    y = monthly["sales"]

    model = LinearRegression()
    model.fit(X,y)

    # Forecast next 3 months
    future_X = np.arange(len(monthly), len(monthly)+3).reshape(-1,1)
    forecast = model.predict(future_X)

    last_month = monthly["month"].max()

    future_months = pd.date_range(
        start=last_month + pd.DateOffset(months=1),
        periods=3,
        freq="M"
    )

    forecast_df = pd.DataFrame({
        "month": future_months,
        "sales": forecast
    })

    return forecast_df