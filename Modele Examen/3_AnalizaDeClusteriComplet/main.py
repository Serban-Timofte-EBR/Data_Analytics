# Analiza de clusteri completa

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

# Citire
df_alcohol = pd.read_csv("data/alcohol.csv")
print("Data csv:")
print(df_alcohol.head())

numeric_cols = df_alcohol.columns[2:]
print("Coloanele numerice: ", numeric_cols)

# Curatare
def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ... ")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_alcohol_clean = cleanData(df_alcohol)

# Standardizare
df_numerics = df_alcohol_clean[numeric_cols]
scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_numerics)

df_data_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_numerics.index,
    columns=df_numerics.columns
)
print("Datele standardizate:")
print(df_data_standardizate)

# Crearea dendogramei
def create_dendogram(data):
    methods = ['ward', 'average', 'single', 'complete']
    linkage_matrices = {}

    for method in methods:
        plt.figure("Dendograma")
        linkage_matrix = linkage(data, method = method)
        linkage_matrices[method] = linkage_matrix
        dendrogram(
            linkage_matrix,
            truncate_mode="lastp",
            p = 10
        )
        plt.title(f"Dendograma {method}")
        plt.xlabel("Sample data")
        plt.ylabel("Distanta")
        plt.show()

    return linkage_matrices

linkage_matrices = create_dendogram(date_standardizate)

# Determinarea numarului optim de clustere
linkage_matrix_ward = linkage_matrices["ward"]
distance = linkage_matrix_ward[:, 2]
differences = np.diff(distance, 2)
punct_elb = np.argmax(differences) + 1
print("Numarul optim de clustere: ", punct_elb)

# Partitionarea
clusters = fcluster(linkage_matrix_ward, t = punct_elb, criterion="maxclust")
df_alcohol["Cluster"] = clusters
print("Dataframe alcohol cu clusteri:")
print(df_alcohol.head())

# Scorul Silhouette
scoreSilhouette = silhouette_score(df_data_standardizate, clusters)
print("Scorul Silhouette: ", scoreSilhouette)

silhouetteVals = silhouette_samples(df_data_standardizate, clusters)
plt.figure("Scor Silhouette")
plt.bar(range(1, len(silhouetteVals) + 1), silhouetteVals)
plt.title("Scor Silhouette")
plt.show()

# Dendograma cu partitia optimala
plt.figure("Dendograma paritia optimala")
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p = 10,
    color_threshold=distance[punct_elb - 1]
)
plt.title(f"Dendograma partitia optimala")
plt.xlabel("Sample data")
plt.ylabel("Distanta")
plt.show()

# Partitia oarecare - Aici este practic acelasi lucru, dar avem un numar dat de clusteri
nr_clusters = 10
clusters_k = fcluster(linkage_matrix_ward, t = nr_clusters, criterion="maxclust")
df_alcohol["Cluster partitia oarecare"] = clusters_k
print("Dataframe alcohol partitia oarecare:")
print(df_alcohol.head())

silhouetteVals_k = silhouette_samples(df_data_standardizate, clusters_k)
plt.figure("Plot Silhouette")
plt.bar(range(1, len(silhouetteVals_k) + 1), silhouetteVals_k)
plt.title("Scor Silhouette")
plt.show()

# Trasare plot partiție în axe principale (partiție optimală și partiție-k) facem analiza ACP
pca = PCA(n_components=2)
C = pca.fit_transform(date_standardizate)

plt.figure("Partitie Optima in Axe PCA")
for cluster in np.unique(clusters):
    plt.scatter(
        C[clusters == cluster, 0],
        C[clusters == cluster, 1],
        label=f"Cluster {cluster}"
    )
plt.title("Partiție optimă în spațiul PCA")
plt.xlabel("Axa PCA 1")
plt.ylabel("Axa PCA 2")
plt.show()
