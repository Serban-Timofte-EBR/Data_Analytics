import pandas as pd

def cleanData(df):
    assert isinstance(df, pd.DataFrame)
    for col in df.columns:
        if df[col].isna().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    return df

def standardizeData(df, numericColumns):
    assert isinstance(df, pd.DataFrame)
    for col in numericColumns:
        if pd.api.types.is_numeric_dtype(df[col]):
            mean = df[col].mean()
            std = df[col].std()
            df[col] = (df[col] - mean) / std
    return df