import pandas as pd
import numpy as np

def calculate_trend(df, date_col, value_col):
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    df["rolling_avg"] = df[value_col].rolling(window=7).mean()

    x = np.arange(len(df))
    y = df[value_col].values

    slope = np.polyfit(x, y, 1)[0]

    return {
        "trend_direction": "upward" if slope > 0 else "downward",
        "slope": slope,
        "rolling_average": df[["rolling_avg"]].dropna().to_dict()
    }
