import pandas as pd
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

# Pasul 2: Separam in categorii
set_barbati = ["Barbati_25-34", "Barbati_35-44", "Barbati_45-64", "Barbati_65_"]
set_femei = ["Femei_18-24", "Femei_35-44", "Femei_45-64", "Femei_65_"]

# Pasul 3: Creem cele doua seturi
X = df_vot_clean[set_barbati]
Y = df_vot_clean[set_femei]

# Ne asiguram de faptul ca X si Y au acelasi numar de randuri
X, Y = X.align(Y, join="inner", axis=0)

# Pasul 4: Analiza canonica
cca = CCA()
cca.fit(X, Y)

# Pasul 5: Scorurile canonice
X_c, Y_c = cca.transform(X, Y)

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

# Pasul 6: Calculam corelatiile canonice
correlation_canonical = cca.score(X, Y)
with open("data/r.csv", "w") as file:
    file.write(f"Corelatia canonica: {correlation_canonical}")

# Pasul 7: Vizualizarea datelor
plt.figure("Vizualizarea datelor canonice")
plt.scatter(X_c[:, 0], X_c[:, 1], label="Barbati")
plt.scatter(Y_c[:, 0], Y_c[:, 1], label="Femei")
plt.title("Primele doua radacii canonice")
plt.xlabel("Componenta 1")
plt.ylabel("Componenta 2")
plt.show()
