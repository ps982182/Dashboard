import pandas as pd

def detect_anomalies(df):

    monthly = df.groupby("month")["sales"].sum().reset_index()

    mean = monthly["sales"].mean()
    std = monthly["sales"].std()

    anomalies = monthly[
        (monthly["sales"] > mean + 2*std) |
        (monthly["sales"] < mean - 2*std)
    ]

    return anomalies