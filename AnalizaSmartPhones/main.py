from data_preparation.data_reader import readData
from data_preparation.data_cleaner import cleanData, cleanDataSmartphones
from data_preparation.data_standardization import standardization

FILE_PATH_SMARTPHONES = "data/Smartphones1.csv"
FILE_PATH_SALES = "data/Iphone_Dataset.csv"

df_smarphones = readData(FILE_PATH_SMARTPHONES)
df_sales = readData(FILE_PATH_SALES)

print("Data:")
print(df_smarphones.head())
print(df_sales.head())

df_smarphones = cleanDataSmartphones(df_smarphones)

df_smarphones = cleanData(df_smarphones)
df_sales = cleanData(df_sales)

df_smarphones.to_csv("data/intermediate/clean/Smartphones_Dataset_cleaned.csv")
df_sales.to_csv("data/intermediate/clean/Iphone_Dataset_cleaned.csv")

numeric_cols_smartphones = [
    'price',
    'rating',
    'Processor_Speed_GHz',
    'Processor_Cores',
    'ram_gb',
    'inbuilt_storage_gb',
    'battery_mAh',
    'display_inches',
    'camera_primary'
]

numeric_cols_sales = [
    'No_of_iPhone_Users',
    'No_of_iPhone_Users_USA',
    'Percentage_of_iPhone_Users',
    'No_of_iPhone_Sold',
    'No_of_iPhone_Sold_USA',
    'iOS_Market_Share',
    'Android_Market_Share'
]

df_smartphones = standardization(df_smarphones, numeric_cols_smartphones)
df_sales = standardization(df_sales, numeric_cols_sales)

df_smartphones.to_csv("data/intermediate/standardized/Smartphones_Dataset_standardized.csv")
df_sales.to_csv("data/intermediate/standardized/Iphone_Dataset_standardized.csv")