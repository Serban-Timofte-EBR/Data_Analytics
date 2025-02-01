import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler

df_global_education = pd.read_csv("data/GlobalEducation.csv", index_col=0)
df_coduri_tari = pd.read_csv("data/CoduriTari.csv", index_col=0)

# Cerinta 1
cerinta1_rows = []
for index, row in df_global_education.iterrows():
    if row["Youth_15_24_Literacy_Rate_Female"] > row["Youth_15_24_Literacy_Rate_Male"]:
        cerinta1_rows.append({
            "CountryId": index,
            "Youth_15_24_Literacy_Rate_Male": row["Youth_15_24_Literacy_Rate_Male"],
            "Youth_15_24_Literacy_Rate_Female": row["Youth_15_24_Literacy_Rate_Female"]
        })
df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/results/Cerinta1.csv", index=False)

# Cerinta 2

df_global_education["Completion"] = (df_global_education["Completion_Primary"] + df_global_education["Completion_Secondary"]) / 2
df_merged = df_global_education.merge(
    df_coduri_tari,
    left_index=True,
    right_index=True
).drop(columns=["Country_y"])
df_merged.to_csv("data/helpers/1_DFMerged.csv")

df_continente = df_merged[["Continent", "Completion"]]
df_completion_by_continent = df_continente.groupby("Continent").mean()
df_completion_by_continent.to_csv("data/results/Cerinta2.csv")

# B - Analiza de clusteri
df_education_2 = pd.read_csv("data/GlobalEducation.csv", index_col=0)
df_education_2 = df_education_2.drop(columns=["Country", "Latitude", "Longitude"])
df_education_2.to_csv("data/helpers/3_DFAnaliza.csv")

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

df_education_clean = cleanData(df_education_2)
print("Clean dataset:")
print(df_education_clean.head())

numeric_cols = df_education_clean.columns[1:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_education_clean[numeric_cols])
print(date_standardizate)

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index = df_education_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/helpers/4_DataStandardizate.csv")

def create_dendogram(data):
    methods = ['ward', 'single', 'complete', 'average']
    linkage_matrices = {}
    for method in methods:
        plt.figure("Dendogram")
        linkage_matrix = linkage(data, method=method)
        linkage_matrices[method] = linkage_matrix
        dendrogram(
            linkage_matrix,
            truncate_mode="lastp",
            p=10
        )
        plt.title(f"Dendrogram {method}")
        plt.show()
    return linkage_matrices

linkage_matrices = create_dendogram(df_date_standardizate)

linkage_matrix_ward = linkage_matrices["ward"]
distances = linkage_matrix_ward[:, 2]
differences = np.diff(distances, 2)
punct_elb = np.argmax(differences) + 1

print("Matricea ward:")
print(linkage_matrix_ward)

print("Distatele: ")
print(distances)

print("Diferentele: ")
print(differences)

print("Punctul Elbow - Numarul optim de clusteri: ", punct_elb)

clusters = fcluster(linkage_matrix_ward, t = punct_elb, criterion="maxclust")
df_education_clean["Cluster"] = clusters
print("Dataframe cu cluster:")
print(df_education_clean.head())
df_education_clean.to_csv("data/results/popt.csv")

plt.figure("Partitia optimala")
dendrogram(
    linkage_matrix_ward,
    truncate_mode="lastp",
    p=10,
    color_threshold=distances[punct_elb - 1],
    above_threshold_color="black"
)
plt.title("Dendrograma partia optimala")
plt.show()

silhScore = silhouette_score(df_date_standardizate, clusters)
print("Scorul Silhouette: ", silhScore)

silhValues = silhouette_samples(df_date_standardizate, clusters)
plt.figure("Scor Silhouette")
plt.bar(range(1, len(silhValues) + 1), silhValues)
plt.title("Scorul Silhouette")
plt.show()