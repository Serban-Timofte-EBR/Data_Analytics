import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

# A
df_edu = pd.read_csv("data/ClusterAnalysisData.csv", index_col=0)

df_edu["GDP_to_Edu_Ratio"] = df_edu["GDP_per_Capita"] / df_edu["EducationExpenditure_per_Capita"]
df_cerinta1 = df_edu.sort_values(by="GDP_to_Edu_Ratio", ascending=False)
df_cerinta1.to_csv("data/results/A/Cerinta1.csv")

df_grouped = df_edu.groupby("Continent")[["HealthcareExpenditure", "InfantMortalityRate"]].mean()
df_grouped.to_csv("data/results/A/Cerinta2.csv")

# B - Analiza de clusteri
df_edu = pd.read_csv("data/ClusterAnalysisData.csv", index_col=0)
analyze_cols = ["GDP_per_Capita", "EducationExpenditure_per_Capita", "HealthcareExpenditure", "InfantMortalityRate"]
df_analysis = df_edu[analyze_cols]

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

df_analysis_clean = cleanData(df_analysis)
df_analysis_clean.to_csv("data/helper/1_DFAnaliza.csv")

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_analysis_clean)

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_analysis_clean.index,
    columns=analyze_cols
)
df_date_standardizate.to_csv("data/results/B/1_DateStandardizate.csv")

def create_dendrogram(data):
    methods = ["single", 'complete', 'average', 'ward']
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
        plt.title(f"Dendrograma cu metoda {method}")
        plt.show()

    return linkage_matrices

linkage_matrices = create_dendrogram(df_date_standardizate)

linkage_matrix_ward = linkage_matrices['ward']
distances = linkage_matrix_ward[:, 2]
differences = np.diff(distances, 2)
punct_elb = np.argmax(differences) + 1

print("Distantele:")
print(distances)

print("Diferentele:")
print(differences)

print("Puntul Elbow - Numarul optim de clusteri: ", punct_elb)

# Partitia optimala
clusters_optimal = fcluster(linkage_matrix_ward, t=punct_elb, criterion="maxclust")
df_analysis_clean["Cluster Optimal"] = clusters_optimal
df_analysis_clean.to_csv("data/results/B/2_PartitiaOptimala.csv")

silhouetteScore = silhouette_score(df_date_standardizate, clusters_optimal)
print("Silhouette Score: ", silhouetteScore)

silhouetteValues = silhouette_samples(df_date_standardizate, clusters_optimal)

plt.figure()
plt.bar(range(1, len(silhouetteValues) + 1), silhouetteValues)
plt.title("Silhouette Values")
plt.show()

plt.figure()
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p=10,
    color_threshold=distances[punct_elb-1],
    above_threshold_color="black"
)
plt.title("Dendrograma partitia optimala")
plt.show()

# Partitia K
nrClusteri = 10
clusters_k = fcluster(linkage_matrix_ward, t=nrClusteri, criterion="maxclust")
df_analysis_clean["Cluster K"] = clusters_k
df_analysis_clean.to_csv("data/results/B/3_PartitiaK.csv")

plt.figure()
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p=10,
    color_threshold=distances[nrClusteri-1],
    above_threshold_color="black"
)
plt.title("Dendrograma partitia k")
plt.show()

silhouetteScoreK = silhouette_score(df_date_standardizate, clusters_k)
print("Silhoette Score K: ", silhouetteScoreK)

silhouetteValuesK = silhouette_samples(df_date_standardizate, clusters_k)
plt.figure()
plt.bar(range(1, len(silhouetteValuesK) + 1), silhouetteValuesK)
plt.title("Silhouette Values - Partitia K")
plt.show()