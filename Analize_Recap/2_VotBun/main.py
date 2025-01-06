import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo

df_vot = pd.read_csv("data/VotBUN.csv", index_col=0)
df_coduri = pd.read_csv("data/Coduri_Localitati.csv", index_col=0)

print("Datele din csv:\n")
print("VotBUN.csv:")
print(df_vot)

print("Coduri_Localitati.csv:")
print(df_coduri)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    print("Curatare date ...")
    if df.isna().any().any():
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_vot = cleanData(df_vot)
df_coduri = cleanData(df_coduri)

df_vot.to_csv("data/1_clean/Vot.csv")
df_coduri.to_csv("data/1_clean/Coduri.csv")

lista_coloane_numerice = list(df_vot.columns[1:])
print("Lista coloanelor numerice:")
print(lista_coloane_numerice)

df_date_numerice = df_vot[lista_coloane_numerice]
print("Dataframe date numerice:")
print(df_date_numerice)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_date_numerice)
print("Date standardizate:")
print(date_standardizate)

df_date_standardizate = pd.DataFrame(
    data = date_standardizate,
    index = df_vot.index,
    columns = lista_coloane_numerice
)
print("Dataframe date standardizate:")
print(df_date_standardizate)
df_date_standardizate.to_csv("data/2_standardizare/Standardizare.csv")

nr_variabile = len(lista_coloane_numerice)
modelAF = FactorAnalyzer(nr_variabile, rotation=None)
F = modelAF.fit(date_standardizate)

scoruri = modelAF.transform(df_date_standardizate)
print("Scoruri: ", scoruri)

etichete = ["F" + str(i+1) for i in range(nr_variabile)]
df_scoruri = pd.DataFrame(
    data=scoruri,
    index=df_date_standardizate.index,
    columns=etichete
)
print("Dataframe scoruri:")
print(df_scoruri)

plt.figure("Scatter scoruri")
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.xlabel("F1")
plt.ylabel("F2")
plt.show()

bartlet = calculate_bartlett_sphericity(df_date_standardizate)
print("Bartlett: ", bartlet[1])

kmo = calculate_kmo(df_date_standardizate)
print("KMO: ", kmo[1])

variance = modelAF.get_factor_variance()
print("Varianta: ", variance)

corelatii_factoriale = modelAF.loadings_
print("Corelatii:", corelatii_factoriale)
df_corelatii = pd.DataFrame(
    data=corelatii_factoriale,
    index=df_date_numerice.columns,
    columns=etichete
)
print("Dataframe corelatii:")
print(df_corelatii)

plt.figure("Heatmap corelatii")
sb.heatmap(df_corelatii)
plt.title("Corelograma corelatii")
plt.show()

comunalitati = modelAF.get_communalities()
print("Comunalitati: ", comunalitati)
df_comunalitati = pd.DataFrame(
    data=comunalitati,
    index=df_date_numerice.columns,
    columns=["Comunalitati"]
)
print("Dataframe comunalitati:")
print(df_comunalitati)

plt.figure("Heatmap comunalitati")
sb.heatmap(df_comunalitati, vmin=0, annot=True)
plt.title("Corelograma comunalitati")
plt.show()