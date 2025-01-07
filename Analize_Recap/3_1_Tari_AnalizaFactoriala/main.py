import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo

df_gdp = pd.read_csv("data/GDP.csv", index_col=0)
df_corruption = pd.read_csv("data/corruption.csv", index_col=0)

print("Datele din csv:")
print("GDP.csv:")
print(df_gdp)

print("corruption.csv:")
print(df_corruption)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    print("Cleaning data ...")
    if df.isna().any().any():
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_gdp = cleanData(df_gdp)
df_corruption = cleanData(df_corruption)

print("Datale curatate:")
print("GDP:")
print(df_gdp)

print("Corruption:")
print(df_corruption)

df_dataset = df_gdp.merge(
    df_corruption,
    left_index=True,
    right_index=True
)
print("Merged data:")
print(df_dataset)
df_dataset.to_csv("data/mergedDF/Dataset.csv")

df_dataset_numeric = df_dataset.select_dtypes(include=['float64', 'int64'])
print("Dataset cu datele numerice:")
print(df_dataset_numeric)
df_dataset_numeric.to_csv("data/mergedDF/DatasetNumeric.csv")

lista_coloane_numerice = list(df_dataset_numeric.columns)
print("Lista coloanelor numerice:")
print(lista_coloane_numerice)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_dataset_numeric)
print("Datele standardizate:")
print(date_standardizate)

df_date_standardizate = pd.DataFrame(
    data=date_standardizate,
    index=df_dataset_numeric.index,
    columns=lista_coloane_numerice
)
print("Dataframe date standardizate:")
print(df_date_standardizate)
df_date_standardizate.to_csv("data/stand/DatasetStandardizat.csv")

nr_var = len(lista_coloane_numerice)
modelFA = FactorAnalyzer(nr_var, rotation=None)
F = modelFA.fit(df_date_standardizate)

etichete = ["F" + str(i+1) for i in range(nr_var)]
print("Etichete: ", etichete)

scoruri = modelFA.transform(df_date_standardizate)

df_scoruri = pd.DataFrame(
    data=scoruri,
    index=df_dataset_numeric.index,
    columns=etichete
)
print("Dataframe scoruri:")
print(df_scoruri)

plt.figure("Scatter scoruri")
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.title("Scatter scoruri")
plt.xlabel("F1")
plt.ylabel("F2")
plt.show()

bartletScore = calculate_bartlett_sphericity(df_date_standardizate)
print("Bartlet Score: ", bartletScore[1])

kmoScore = calculate_kmo(df_date_standardizate)
print("KMO: ", kmoScore[1])

variance = modelFA.get_factor_variance()
print("Variance: ", variance)

corelatii = modelFA.loadings_
df_corelatii = pd.DataFrame(
    data=corelatii,
    index=lista_coloane_numerice,
    columns=etichete
)
print("Dataframe corelatii")
print(df_corelatii)

plt.figure("Heatmap corelatii")
sb.heatmap(df_corelatii)
plt.show()

comunalitati = modelFA.get_communalities()
df_comunalitati = pd.DataFrame(
    data=comunalitati,
    index=lista_coloane_numerice,
    columns=["Comunalitati"]
)

plt.figure("Heatmap comunalitati")
sb.heatmap(df_comunalitati, annot=True)
plt.show()