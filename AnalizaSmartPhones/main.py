import threading

from data_preparation.data_reader import readData
from data_preparation.data_cleaner import cleanData, cleanDataSmartphones
from data_preparation.data_standardization import standardization

FILE_PATH_SMARTPHONES = "data/Smartphones1.csv"
FILE_PATH_SALES = "data/Iphone_Dataset.csv"

def process_smartphones():
    df_smartphones = readData(FILE_PATH_SMARTPHONES)
    df_smartphones = cleanDataSmartphones(df_smartphones)
    df_smartphones = cleanData(df_smartphones)
    df_smartphones.to_csv("data/intermediate/clean/Smartphones_Dataset_cleaned.csv")

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

    df_smartphones = standardization(df_smartphones, numeric_cols_smartphones)
    df_smartphones.to_csv("data/intermediate/standardized/Smartphones_Dataset_standardized.csv")

def process_sales():
    df_sales = readData(FILE_PATH_SALES)
    df_sales = cleanData(df_sales)
    df_sales.to_csv("data/intermediate/clean/Iphone_Dataset_cleaned.csv")

    numeric_cols_sales = [
        'No_of_iPhone_Users',
        'No_of_iPhone_Users_USA',
        'Percentage_of_iPhone_Users',
        'No_of_iPhone_Sold',
        'No_of_iPhone_Sold_USA',
        'iOS_Market_Share',
        'Android_Market_Share'
    ]

    df_sales = standardization(df_sales, numeric_cols_sales)
    df_sales.to_csv("data/intermediate/standardized/Iphone_Dataset_standardized.csv")

thread_smartphones = threading.Thread(target=process_smartphones)
thread_sales = threading.Thread(target=process_sales)

thread_smartphones.start()
thread_sales.start()

thread_smartphones.join()
thread_sales.join()

print("Data preparation completed!")