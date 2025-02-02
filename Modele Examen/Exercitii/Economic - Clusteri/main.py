import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

df_econonic = pd.read_csv("data/EconomicDevelopment.csv", index_col=0)
df_regions = pd.read_csv("data/RegionMapping.csv", index_col=0)

# Cerința 1: Să se determine țările care au o rată a șomajului mai mică de 5% și o speranță de viață mai mare de 75 de ani.
# Rezultatele să fie salvate într-un fișier numit LowUnemployment_HighLifeExpectancy.csv și să conțină coloanele:

df_filtered = df_econonic[df_econonic["UnemploymentRate"] < 5]
df_filtered_2 = df_filtered[df_filtered["LifeExpectancy"] > 75]
df_cerinta1 = df_filtered_2[["UnemploymentRate", "LifeExpectancy"]]
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Cerința 2: Să se calculeze media PIB-ului și a cheltuielilor pentru sănătate pe regiuni.
# Rezultatele să fie salvate într-un fișier numit RegionStatistics.csv cu următoarele coloane:
df_merged = df_econonic.merge(
    df_regions,
    left_index=True,
    right_index=True
)
df_merged.to_csv("data/helpers/1_Merged.csv", index=False)

df_grouped = df_merged.groupby("Region").mean()

df_cerinta2 = df_grouped[["GDP", "HealthExpenditure"]].rename(columns={"GDP": "GDP_Mean", "HealthExpenditure":"HealthExpenditure_Mean"})
df_cerinta2.to_csv("data/results/Cerinta2.csv")

# Partea B: Analiza Clusterelor
df_econonic = pd.read_csv("data/EconomicDevelopment.csv", index_col=0)

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

df_econonic_clean = cleanData(df_econonic)
print("DF Economic:")
print(df_econonic_clean.head())

numeric_cols = ["GDP", "UnemploymentRate", "LifeExpectancy", "EducationExpenditure", "HealthExpenditure"]

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_econonic_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_econonic_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/helpers/2_Stand.csv")

def create_dendrogram(data):
    methods = ['ward', 'complete', 'average', 'single']
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

print("Distances:")
print(distances)

print("Differences:")
print(differences)

print("Punctul Elbow - Numarul optim de clusteri: ", punct_elb)

plt.figure()
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p=10,
    color_threshold=distances[punct_elb - 1],
    above_threshold_color="black"
)
plt.title(f"Dendrograma partiei optimale")
plt.show()

clusters = fcluster(linkage_matrix_ward, criterion="maxclust", t=punct_elb)
print("Clusters:")
print(clusters)
df_econonic_clean["Cluster"] = clusters
df_econonic_clean.to_csv("data/results/Clusters.csv")

silhouetteScoer = silhouette_score(df_date_standardizate, clusters)
print("Silhouette Score: ", silhouetteScoer)

silhouetteValues = silhouette_samples(df_date_standardizate, clusters)
plt.figure()
plt.bar(range(1, len(silhouetteValues) + 1), silhouetteValues)
plt.title("Grafic Silhouette Score")
plt.show()

# Partitia oarecare
nrClusteri = 4
clusters_oarecare = fcluster(linkage_matrix_ward, t = nrClusteri, criterion="maxclust")
print("Clusteri oarecare: ", clusters_oarecare)

df_econonic_clean["Clusteri Oarecare"] = clusters_oarecare
df_econonic_clean.to_csv("data/results/ClusteriOarecare.csv")

silhouetteScoer = silhouette_score(df_date_standardizate, clusters_oarecare)
print("Silhouette Score: ", silhouetteScoer)

silhouetteValues = silhouette_samples(df_date_standardizate, clusters_oarecare)
plt.figure()
plt.bar(range(1, len(silhouetteValues) + 1), silhouetteValues)
plt.title("Grafic Scorurile Silhouette - Partitia oarecare")
plt.show()