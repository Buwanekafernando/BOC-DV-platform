import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

def forecast_time_series(df, date_col, value_col, periods=12):
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    series = df.set_index(date_col)[value_col]

    model = ARIMA(series, order=(1,1,1))
    fitted = model.fit()

    forecast = fitted.forecast(steps=periods)

    return {
        "history": series.tail(50).to_dict(),
        "forecast": forecast.to_dict()
    }
