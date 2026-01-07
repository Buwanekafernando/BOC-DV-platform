import numpy as np

def detect_anomalies(df, value_col, threshold=3):# Using Z-score method
    mean = df[value_col].mean()
    std = df[value_col].std()
    

    df["z_score"] = (df[value_col] - mean) / std
    anomalies = df[df["z_score"].abs() > threshold]
    

    return anomalies[[value_col]].to_dict()
# The function detects anomalies in the specified value column of the dataframe using the Z-score method.


