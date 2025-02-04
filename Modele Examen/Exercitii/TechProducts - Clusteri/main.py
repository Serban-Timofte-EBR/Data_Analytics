import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageChops import difference
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

df_products = pd.read_csv("data/TechProducts.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ...")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_products_clean = cleanData(df_products)
numeric_cols = df_products_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_products_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_products_clean.index,
    columns=numeric_cols
)
print("Date Standardizate:")
print(df_date_standardizate)

def create_dendrogram(data):
    methods = ["single", "complete", "average", "ward"]
    linkage_matrices = {}

    for method in methods:
        linkage_matrix = linkage(data, method=method)
        linkage_matrices[method] = linkage_matrix

        plt.figure()
        dendrogram(
            linkage_matrix,
            truncate_mode="lastp",
            p=10
        )
        plt.title(f"Dendrograma {method}")
        plt.show()

    return linkage_matrices

linkage_matrices = create_dendrogram(df_date_standardizate)

linkage_matrix_ward = linkage_matrices["ward"]
distances = linkage_matrix_ward[:, 2]
differences = np.diff(distances, 2)
punct_elb = np.argmax(differences) + 1

print("Distantele:")
print(distances)

print("Diferentele:")
print(differences)

print("Punctul Elbow - Numarul optim de clusteri: ", punct_elb)

clusters = fcluster(linkage_matrix_ward, t=punct_elb, criterion="maxclust")
df_products_clean["Cluster - Partitia optimala"] = clusters
df_products_clean.to_csv("data/RESULT_1_PartitiaOptimala.csv")

plt.figure()
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p=10,
    color_threshold=distances[punct_elb-1],
    above_threshold_color="black"
)
plt.title("Partitia Optimala")
plt.show()

silhouetteScore = silhouette_score(df_date_standardizate, clusters)
print("Scor Silhouette: ", silhouetteScore)

silhouetteSample = silhouette_samples(df_date_standardizate, clusters)
plt.figure()
plt.bar(range(1, len(silhouetteSample) + 1), silhouetteSample)
plt.title("Valorile Silhouette")
plt.show()

kClust = 13
clusters_k = fcluster(linkage_matrix_ward, t=kClust, criterion="maxclust")
df_products_clean["Cluster - Partitia K"] = clusters_k
df_products_clean.to_csv("data/RESULT_2_Partitiak.csv")

plt.figure()
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p=10,
    color_threshold=distances[kClust-1],
    above_threshold_color="black"
)
plt.title("Partitia K")
plt.show()