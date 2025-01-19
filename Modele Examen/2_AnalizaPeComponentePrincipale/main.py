import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df_mise = pd.read_csv("data/MiseNatPopTari.csv", index_col=0)
df_coduriTari = pd.read_csv("data/CoduriTariExtins.csv", index_col=0)

print("Dataframe-uri:")
print(df_mise)
print(df_coduriTari)

# Cerinta A - Ex. 1
numeric_cols = ["RS", "FR", "LM", "MMR", "LE", "LEM", "LEF"]
df_mise["Medie"] = df_mise[numeric_cols].mean(axis=1)

df_cerinta_1 = df_mise[["Three_Letter_Country_Code", "Medie"]]

print("Dataframe cu medii:")
print(df_cerinta_1)
df_cerinta_1.to_csv("data/1_cerinta/cerinta1.csv", index=False)

# Cerinta A - Ex. 2
df_merged = df_mise.merge(
    df_coduriTari,
    left_index=True,
    right_index=True
)
print("Datafram merged:")
print(df_merged)
df_merged = df_merged.drop(columns = ["Country_Name_y"])
df_merged.to_csv("data/helper/MergedDataframe.csv")

df_continente = df_merged.groupby("Continent")[numeric_cols].mean()
print("Dataframe continente")
print(df_continente)

# df_cerinta_2 = pd.DataFrame({
#     "Continent": df_continente.index,
#     "Coloana:": df_continente.idxmax(axis = 1)
# })
# print("Dataframe cerinta 2:")
# print(df_cerinta_2)

df_cerinta_2 = pd.DataFrame({
    "Coloana": df_continente.columns,
    "Continent": df_continente.idxmax()
})
print("Dataframe cerinta 2:")
print(df_cerinta_2)
df_cerinta_2.to_csv("data/2_cerinta/cerinta2.csv", index=False)

# Cerinta B - Analiza ACP
def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Clean data ...")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_data_clean = cleanData(df_merged)
print("Dataframe pentru analiza ACP:")
print(df_data_clean)
df_data_clean.to_csv("data/helper/DateAnalizaACP.csv")

df_date_numerice = df_data_clean[numeric_cols]
print("Dataframe numeric:")
print(df_date_numerice)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_date_numerice)
print("Date standardizate:")
print(date_standardizate)

modelACP = PCA()
C = modelACP.fit_transform(date_standardizate)
etichetePCA = ["C" + str(i+1) for i in range(C.shape[1])]

variance = modelACP.explained_variance_ratio_
print("Variance ration: ", variance)

df_variance = pd.DataFrame({
    "Componenta": etichetePCA,
    "Explained_Variance": variance
})
print("Dataframe cu variația explicată:")
print(df_variance)
df_variance.to_csv("data/3_cerinta/pca_variance.csv", index=False)

df_pca = pd.DataFrame(
    C,
    index=df_merged["Country_Name_x"],
    columns=etichetePCA
)
print("Dataframe PCA:")
print(df_pca)
df_cerinta_3 = df_pca.drop(columns=["C3", "C4"])
df_cerinta_3.to_csv("data/3_cerinta/pca_projection.csv")

plt.figure("Scatter ACP")
plt.scatter(df_pca["C1"], df_pca["C2"], color = 'y')
plt.xlabel("C1")
plt.ylabel("C2")
plt.title("Scatter ACP")
plt.show()

matrice_corelatii = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
df_corelatii = pd.DataFrame(
    matrice_corelatii,
    index=df_date_numerice.columns,
    columns=etichetePCA
)
print("Dataframe corelatii")
print(df_corelatii)

plt.figure("Heatmap corelatii")
sb.heatmap(df_corelatii)
plt.title("Heatmap corelatii")
plt.show()

comunalities = np.cumsum(matrice_corelatii ** 2, axis=1)
df_comunalitati = pd.DataFrame(
    comunalities,
    index = df_date_numerice.columns,
    columns=etichetePCA
)
print("Dataframe comunalitati:")
print(df_comunalitati)

plt.figure("Heatmap comunalitati")
sb.heatmap(df_comunalitati)
plt.title("Heatmap comunalitati")
plt.show()