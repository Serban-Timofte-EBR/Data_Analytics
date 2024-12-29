import pandas as pd
import matplotlib.pyplot as plt
import os

def standardization(df, numeric_cols):
    assert isinstance(df, pd.DataFrame)
    print("Standardizing data...")
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = (df[col] - mean) / std
    return df

def save_descriptive_statistics(df, numeric_columns, output_file):
    assert isinstance(df, pd.DataFrame)
    assert all(col in df.columns for col in numeric_columns)

    charts_dir = os.path.join(os.path.dirname(output_file), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    with open(output_file, "w") as file:
        file.write("Descriptive Statistics:\n")
        file.write("=" * 40 + "\n")
        stats = df[numeric_columns].describe().transpose()
        file.write(stats.to_string())
        file.write("\n")
    print(f"Descriptive statistics saved to {output_file}")

    for col in numeric_columns:
        plt.figure(figsize=(10, 6))
        plt.hist(df[col].dropna(), bins=30, color='blue', alpha=0.7, edgecolor='black')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        chart_path = os.path.join(charts_dir, f"{col}_distribution.png")
        plt.savefig(chart_path)
        plt.close()
        print(f"Chart for {col} saved to {chart_path}")