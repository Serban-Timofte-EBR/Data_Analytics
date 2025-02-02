import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

df_economic = pd.read_csv("data/EconomicDemographicData.csv", index_col=0)
df_continente = pd.read_csv("data/ContinentCodes.csv", index_col=0)

# Să se determine țările unde PIB-ul pe cap de locuitor (GDP_per_Capita)
# este mai mare decât rata medie a șomajului pe continentul corespunzător.
df_merged = df_economic.merge(
    df_continente,
    left_index=True,
    right_index=True
)
df_merged.to_csv("data/helpers/1_Merge.csv")

df_filtered = df_merged[df_merged["GDP_per_Capita"] > df_merged["UnemploymentRate"]]
df_cerinta1 = df_filtered[["GDP_per_Capita", "UnemploymentRate", "Continent"]]
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Să se determine continentul care are cea mai mică variație standard pentru rata șomajului.
df_grouped = df_merged.groupby("Continent").std()
df_grouped.to_csv("data/helpers/2_Grouped.csv")

continentMin = df_grouped["UnemploymentRate"].idxmin()
valStdMin = df_grouped.loc[continentMin, "UnemploymentRate"]
print("Continentul cu cea mai mica variatie standard pentru rata somajului este: ", continentMin)
print("Valoarea este: ", valStdMin)

# Partea B - Analiza de clusteri
df_economic = pd.read_csv("data/EconomicDemographicData.csv", index_col=0)

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

df_economic_clean = cleanData(df_economic)
df_economic_clean.to_csv("data/helpers/3_Clean.csv")

numeric_cols = df_economic_clean.columns[0:]
print("Numeric columns: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_economic_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_economic_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/helpers/4_Stand.csv")

def create_dendrogram(data):
    methods = ['complete', 'single', 'average', 'ward']
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
print("Matricea ierarhica:")
print(linkage_matrix_ward)
df_linkage = pd.DataFrame(
    linkage_matrix_ward,
    columns=["Cluster1", "Cluster2", "Distance", "ClusterSize"]
)
print(df_linkage)

distances = linkage_matrix_ward[:, 2]
differences = np.diff(distances, 2)
punct_elb = np.argmax(differences) + 1

print("Distantele: ", distances)
print("Diferentele: ", differences)
print("Puntul Elbow - Numarul optim de cluster: ", punct_elb)

clusters = fcluster(linkage_matrix_ward, t = punct_elb, criterion="maxclust")
df_economic_clean["Cluster Optim"] = clusters
df_economic_clean.to_csv("data/results/PartitiaOptimala.csv")

scorSilhouette = silhouette_score(df_date_standardizate, clusters)
print("Scorul Silhoette: ", scorSilhouette)

valoriSilhouette = silhouette_samples(df_date_standardizate, clusters)
print("Valorile Silhouette: ", valoriSilhouette)

plt.figure()
plt.bar(range(1, len(valoriSilhouette) + 1), valoriSilhouette)
plt.title("Bar chart valori Silhouette")
plt.show()
