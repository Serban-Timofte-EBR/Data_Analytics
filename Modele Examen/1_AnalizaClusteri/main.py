import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler

df_alcohol = pd.read_csv("data/alcohol.csv", index_col=0)
df_tariExtins = pd.read_csv("data/CoduriTariExtins.csv", index_col=0)

print("Dataframe Alcool:")
print(df_alcohol)

print("Dataframe Tari Extins:")
print(df_tariExtins)

# ----------------- Cerința A -----------------
# 1: Media pe tari
numeric_cols = ['2000', '2005', '2010', '2015', '2018']
df_alcohol["Medie"] = df_alcohol[numeric_cols].mean(axis=1)

cols_cerinta_1 = ["Code", "Medie"]
df_cerinta1 = df_alcohol[cols_cerinta_1]
df_cerinta1.to_csv("data/1_cerinta/cerinta1.csv", index=False)

# 2: Cea mai mare medie pe continente
df_alcohol_tariExtins = df_alcohol.merge(
    df_tariExtins,
    left_index=True,
    right_index=True
)

print("Dataframe Merge:")
print(df_alcohol_tariExtins)

df_continente = df_alcohol_tariExtins.groupby("Continent")[numeric_cols].mean()
print("Dataframe continente:")
print(df_continente)

df_cerinta2 = pd.DataFrame({
    "Continent_Name": df_continente.index,
    "Anul": df_continente.idxmax(axis = 1)
})
print("Dataframe cerinta 2:")
print(df_cerinta2)
df_cerinta2.to_csv("data/2_cerinta/cerinta2.csv", index=False)

# ----------------- Cerința B -----------------
print("Dataframes cerinta B:")
print(df_alcohol)
print(df_tariExtins)

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

df_alcohol_clean = cleanData(df_alcohol)
print("Datagrame curatat:")
print(df_alcohol_clean)

df_numeric = df_alcohol_clean[numeric_cols]

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_numeric)
print("Data standardizate:")
print(date_standardizate)

df_standardizat = pd.DataFrame(
    date_standardizate,
    index = df_numeric.index,
    columns=df_numeric.columns
)
print("Dataframe date standardizate:")
print(df_standardizat)

linkage_matrix = linkage(df_standardizat, method="ward")
df_linkage_matrix = pd.DataFrame(
    linkage_matrix,
    columns=["Cluster_1", "Cluster_2", "Distanta", "Numar_instante"]
)
print("Matricea de ierarhie: ")
print(df_linkage_matrix)

plt.figure("Dendrogram Ward")
dendrogram(
    linkage_matrix,
    p = 10,
    truncate_mode="lastp"
)
plt.title("Dendrogram Ward")
plt.show()

distances = linkage_matrix[:, 2]
dif = np.diff(distances, 2)
punct_elb = np.argmax(dif) + 2
print("Numarul optim de clusteri: ", punct_elb)

clusters = fcluster(linkage_matrix, t = punct_elb, criterion="maxclust")
df_alcohol_clean["Cluster"] = clusters
print("Dataframe cu clusters:")
print(df_alcohol_clean)

