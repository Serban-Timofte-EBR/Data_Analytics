import pandas as pd

def standardization(df, numeric_cols):
    assert isinstance(df, pd.DataFrame)
    print("Standardizing data...")
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = (df[col] - mean) / std
    return df