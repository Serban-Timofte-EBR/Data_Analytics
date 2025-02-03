import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageChops import difference
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

df_economic = pd.read_csv("data/EconomicTradeData.csv", index_col=0)

# Consumul de energie pe cap de locuitor la nivel de tara
df_cerinta1 = df_economic.copy()
df_cerinta1["EnergyConsumptionPerCapita"] = df_cerinta1["EnergyConsumption"] / df_cerinta1["Population"]
df_cerinta1 = df_cerinta1.sort_values(by="EnergyConsumptionPerCapita", ascending=False)
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Consumul de energie pe cap de locuitor la nivel de continent
df_grouped = df_economic.groupby("Continent").sum()
df_grouped.to_csv("data/helpers/1_Grouped.csv")
df_grouped["EnergyConsumptionPerCapita"] = df_grouped["EnergyConsumption"] / df_grouped["Population"]
df_grouped = df_grouped.sort_values(by="EnergyConsumptionPerCapita", ascending=False)
df_grouped.to_csv("data/results/Cerinta2.csv")

# Determinarea continentului cu cea mai mică variație standard a ratei șomajului
df_std = df_economic.groupby("Continent")["UnemploymentRate"].std()
df_std = df_std.reset_index().rename(columns={"UnemploymentRate": "StandardDev"})

df_std_sorted = df_std.sort_values(by="StandardDev", ascending=True)
df_std_sorted.to_csv("data/helpers/2_Std.csv", index=False)

df_cerinta3 = df_std_sorted.head(1)
df_cerinta3.to_csv("data/results/Cerinta3.csv", index=False)

# B - Analiza de clusteri

df_cluster = pd.read_csv("data/EconomicClusteringData.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ... ")
        for col in df.columns:
            if df[col].isna().any().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_cluster_clean = cleanData(df_cluster)
numeric_cols = df_cluster_clean.columns[0:]
print("numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_cluster_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_cluster_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/B_1_ClusteringStandardized.csv")

def create_dendrogram(data):
    methods = ['single', 'complete', 'average', 'ward']
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
linkage_matrix_ward = linkage_matrices['ward']

distances = linkage_matrix_ward[:, 2]
differences = np.diff(distances, 2)
punct_elb = np.argmax(differences) + 1

print("Distantele:")
print(distances)

print("Diferentele")
print(differences)

print("Punctul Elb - Numarul optim de clusteri: ", punct_elb)

# Partitia optimala
clusters = fcluster(linkage_matrix_ward, t = punct_elb, criterion="maxclust")
df_cluster_clean["Cluster Optim"] = clusters
df_cluster_clean.to_csv("data/results/B_2_ClusteringResults.csv")

silhouetteScore =  silhouette_score(df_cluster_clean, clusters)
print("Scorul Silhouette: ", silhouetteScore)

silhouetteValues = silhouette_samples(df_cluster_clean, clusters)
plt.figure()
plt.bar(range(1, len(silhouetteValues) + 1), silhouetteValues)
plt.title("Silhouette Values")
plt.show()