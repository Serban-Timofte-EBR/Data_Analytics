import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.preprocessing import StandardScaler

def load_data():
    df = pd.read_csv('mortalitate_ro.csv')
    return df

def clean_data(df):
    assert isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

def split_data(data):
    assert isinstance(data, pd.DataFrame)
    numeric_values = data.iloc[:, 2:].values
    judete = data['Judet'].values

    return numeric_values, judete

def standardize_data(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def create_dendogram(data):
    methods = ['single', 'complete', 'average', 'ward']
    for i, method in enumerate(methods, 1):
        plt.figure(figsize=(20, 10))
        plt.subplot(2, 2, i)

        Z = linkage(data, method = method)
        dendrogram(
            Z,
            truncate_mode='lastp',
            p = 10,
            leaf_rotation=90.,
            leaf_font_size=8.,
            show_leaf_counts=True,
        )

        plt.title(f'Diagrama de clusterizare ierarhica cu metoda: {method}')
        plt.xlabel('Sample index')
        plt.ylabel('Distanta')

        plt.tight_layout()
        plt.show()

def cluster_analytics():
    mortalitate = load_data();
    mortalitateClean = clean_data(mortalitate)
    X, judete = split_data(mortalitateClean)
    X_scaled = standardize_data(X)
    create_dendogram(X_scaled)

cluster_analytics()