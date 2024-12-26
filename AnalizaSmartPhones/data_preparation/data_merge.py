import pandas as pd

def combine_datasets(FILE_PATH_SMARTPHONES, FILE_PATH_SALES):
    df_smartphones = pd.read_csv(FILE_PATH_SMARTPHONES)
    df_sales = pd.read_csv(FILE_PATH_SALES)

    relevant_columns = ['os_type', 'iOS_Market_Share', 'Android_Market_Share']
    df_sales_relevant = df_sales[relevant_columns].drop_duplicates(subset='os_type')

    df_combined = pd.merge(
        df_smartphones,
        df_sales_relevant,
        on='os_type',
        how='left'
    )

    df_combined.fillna(0, inplace=True)

    df_combined.to_csv("data/intermediate/analysis/Smartphones_With_Market_Data.csv", index=False)
    print(f"Final dataset saved")