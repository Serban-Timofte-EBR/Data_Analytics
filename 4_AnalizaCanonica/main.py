import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cross_decomposition import CCA


df_vot = pd.read_csv("data/Vot.csv", index_col=0)
df_coduri = pd.read_csv("data/Coduri_localitati.csv", index_col=0)

print("Datele din csv:")
print(df_vot.head())
print(df_coduri.head())

# Partea A

# Cerinta 1 - procentele participarii pe categorii de varsta

coloane_numerice = df_vot.select_dtypes(include=['int64', 'float64']).columns
coloane_numerice_analiza = coloane_numerice.drop(["Votanti_LP"])
print("Coloanele relevante: ", coloane_numerice_analiza)

cerinta1_rows = []

for index, row in df_vot.iterrows():
    votanti_lp = row["Votanti_LP"]
    row_procente = (row[coloane_numerice_analiza] * 100) / votanti_lp

    cerinta1_rows.append({
        "Siruta": index,
        "Localitatea": row["Localitate"],
        **row_procente
    })

df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/cerinta1.csv", index=False)

# Cerinta 2 - Media participarii pe judete

df_merged = df_vot.merge(
    df_coduri,
    left_index=True,
    right_index=True
).drop(columns=["Localitate_y", "Mediu"])

df_merged_jud = df_merged.groupby("Judet").sum()
df_merged_jud = df_merged_jud.drop(columns=["Localitate_x"])

cerinta2_rows = []
for index, row in df_merged_jud.iterrows():
    votanti_lp = row["Votanti_LP"]
    procente_row = row[coloane_numerice_analiza] * 100 / votanti_lp

    cerinta2_rows.append({
        "Judet": index,
        **procente_row
    })

df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/cerinta2.csv", index=False)

# B - Analiza canonica

print("Datele pentru analiza:")
print(df_vot)

# Pasul 1: Curatam datele
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

df_vot_clean = cleanData(df_vot)

# 3. Separarea variabilelor în categorii
set_barbati = ["Barbati_25-34", "Barbati_35-44", "Barbati_45-64", "Barbati_65_"]
set_femei = ["Femei_18-24", "Femei_35-44", "Femei_45-64", "Femei_65_"]

X = df_vot_clean[set_barbati]
Y = df_vot_clean[set_femei]

# Ne asiguram ca sunt egale
X, Y = X.align(Y, join="inner", axis=0)

# Analiza canonica
modelCCA = CCA(n_components=2)
X_c, Y_c = modelCCA.fit_transform(X, Y)
df_X_c = pd.DataFrame(
    X_c,
    index=X.index,
    columns=["X_c1", "X_c2"]
)
df_X_c.to_csv("data/z.csv")

df_Y_c = pd.DataFrame(
    Y_c,
    index=Y.index,
    columns=["Y_c1", "Y_c2"]
)
df_Y_c.to_csv("data/u.csv")


# Corelatiile canonice
corelatii_canonice = modelCCA.score(X, Y)
print("Corelatia canonica: ", corelatii_canonice)

# Instanțe în spațiile celor două variabile canonice
plt.figure("Vizualizarea datelor canonice")
plt.scatter(X_c[:, 0], X_c[:, 1], label="Barbati")
plt.scatter(Y_c[:, 0], Y_c[:, 1], label="Femei")
plt.title("Primele doua radacii canonice")
plt.xlabel("Componenta 1")
plt.ylabel("Componenta 2")
# plt.show()

# Corelograma
corr_x = np.corrcoef(X.T, X_c.T)[:X.shape[1], X.shape[1]:]
corr_y = np.corrcoef(Y.T, Y_c.T)[:Y.shape[1], Y.shape[1]:]

df_corr_x = pd.DataFrame(
    corr_x,
    index=set_barbati,
    columns=["X_c1", "X_c2"]
)
print(df_corr_x.head())

df_corr_y = pd.DataFrame(
    corr_y,
    index=set_femei,
    columns=["Y_c1", "Y_c2"]
)
print(df_corr_y.head())

plt.figure("Corelograma 1")
sns.heatmap(df_corr_x)
plt.title("Corelograma variabilei X in variabile canonice")
plt.show()

plt.figure("Corelograma 2")
sns.heatmap(df_corr_y)
plt.title("Corelograma variabilei Y in variabile canonice")
plt.show()

C -> lucrul cu Dataframe-uri (extra)

df_vot_nou = pd.read_csv("data/Vot.csv", index_col=0)
df_coduri_nou = pd.read_csv("data/Coduri_localitati.csv", index_col=0)

print("Datele din csv:")
print(df_vot_nou.head())
print(df_coduri_nou.head())

# Totalul participării pe categorii de vârstă pe județe
df_merged_nou = df_vot_nou.merge(
    df_coduri_nou,
    right_index=True,
    left_index=True
).drop(columns=["Localitate_y", "Mediu"])
print("Dataframe merged nou:")
print(df_merged_nou.head())

df_pe_judete = df_merged_nou.groupby("Judet").sum().drop(columns=["Localitate_x"])
df_pe_judete.to_csv("data/C/cerinta3.csv")

# Diferența dintre participarea bărbaților și femeilor pe localități
    # Pentru fiecare localitate, să se calculeze diferența dintre totalul participării bărbaților și femeilor (Barbati_* și Femei_*)
cerinta4_rows=[]
for index, row in df_vot_nou.iterrows():
    nr_barbati = row[set_barbati].sum()
    nr_femei = row[set_femei].sum()
    diff = nr_barbati - nr_femei

    cerinta4_rows.append({
        "Siruta": index,
        "Localitate": row["Localitate"],
        "Diferenta_Barbati_Femei": diff
    })

# df_cerinta4 = pd.DataFrame(cerinta4_rows).sort_values(by="Localitate", ascending=True)
df_cerinta4 = pd.DataFrame(cerinta4_rows).sort_values(by="Diferenta_Barbati_Femei", ascending=False)
df_cerinta4.to_csv("data/C/cerinta4.csv", index=False)

# Procentul total de participare urban vs. rural
    # Mediu,Procent_Participare
    # Urban,75.5
    # Rural,24.5
df_merged_nou_mediu = df_vot_nou.merge(
    df_coduri_nou,
    right_index=True,
    left_index=True
).drop(columns=["Localitate_y"])

df_groupBy_mediu = df_merged_nou_mediu.groupby("Mediu").sum().drop(columns=["Localitate_x", "Judet"])

coloane_votanti = df_groupBy_mediu.loc[:, "Barbati_25-34":].columns
print("Coloanele de votanti: ", coloane_votanti)

cerinta5_rows=[]
for index, row in df_groupBy_mediu.iterrows():
    totalVotanti = row[coloane_votanti].sum()
    print(f"{index} - Total Votanți: {totalVotanti}, Votanți LP: {row['Votanti_LP']}")
    prezenta = totalVotanti / row["Votanti_LP"] * 100

    cerinta5_rows.append({
        "Mediu": index,
        "Procent_Participare": prezenta
    })

df_cerinta5 = pd.DataFrame(cerinta5_rows)
df_cerinta5.to_csv("data/C/cerinta5.csv", index=False)
