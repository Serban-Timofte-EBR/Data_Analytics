import threading

import pandas as pd

from data_preparation.data_reader import readData
from data_preparation.data_cleaner import cleanData, cleanDataSmartphones
from data_preparation.data_standardization import standardization, save_descriptive_statistics
from data_preparation.data_merge import combine_datasets
from pca.analysis import pca, visualize, kmeans_clustering

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
        'camera_primary',
        'resolution_width',
        'resolution_height'
    ]

    save_descriptive_statistics(
        df_smartphones, numeric_cols_smartphones,
        "data/statistics/smartphones_statistics.txt"
    )

    df_smartphones = standardization(df_smartphones, numeric_cols_smartphones)
    df_smartphones.to_csv("data/intermediate/standardized/Smartphones_Dataset_standardized.csv")

def process_sales():
    df_sales = readData(FILE_PATH_SALES)
    df_sales['os_type'] = df_sales.apply(
        lambda row: 'ios' if row['iOS_Market_Share'] > row['Android_Market_Share'] else 'android',
        axis=1
    )
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

    save_descriptive_statistics(
        df_sales, numeric_cols_sales,
        "data/statistics/sales_statistics.txt"
    )

    df_sales = standardization(df_sales, numeric_cols_sales)
    df_sales.to_csv("data/intermediate/standardized/Iphone_Dataset_standardized.csv")

thread_smartphones = threading.Thread(target=process_smartphones)
thread_sales = threading.Thread(target=process_sales)

thread_smartphones.start()
thread_sales.start()

thread_smartphones.join()
thread_sales.join()

print("Data preparation completed!")

df_smartphones = pd.read_csv("data/intermediate/standardized/Smartphones_Dataset_standardized.csv")
df_sales = pd.read_csv("data/intermediate/standardized/Iphone_Dataset_standardized.csv")
print("Smartphones dataset head:\n", df_smartphones.head())
print("Sales dataset head:\n", df_sales.head())

FILE_PATH_SMARTPHONES_STAND = "data/intermediate/standardized/Smartphones_Dataset_standardized.csv"
FILE_PATH_SALES_STAND = "data/intermediate/standardized/Iphone_Dataset_standardized.csv"

FILE_PATH_FINAL_DATASET = "data/intermediate/analysis/Smartphones_With_Market_Data.csv"
FILE_PATH_PCA_RESULTS = "data/pca/PCA_Results.csv"

combine_datasets(FILE_PATH_SMARTPHONES_STAND, FILE_PATH_SALES_STAND)

df_combined = pd.read_csv(FILE_PATH_FINAL_DATASET)
print("Combined dataset head:\n", df_combined.head())

numeric_columns_pca = [
    'price', 'rating', 'Processor_Speed_GHz', 'Processor_Cores',
    'ram_gb', 'inbuilt_storage_gb', 'battery_mAh', 'display_inches',
    'camera_primary', 'resolution_width', 'resolution_height',
    'iOS_Market_Share', 'Android_Market_Share'
]

df_pca, explained_variance = pca(df_combined, numeric_columns_pca, FILE_PATH_PCA_RESULTS)

num_clusters = 4
clusters = kmeans_clustering(df_pca[['PC1', 'PC2']], num_clusters)

print("PCA analysis completed.")
print(f"Explained variance ratio: {explained_variance}")

visualize(df_pca, 'PC1', 'PC2', clusters)