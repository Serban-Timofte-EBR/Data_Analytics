import warnings
from statistics import variance

warnings.filterwarnings("ignore")

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from factor_analyzer import calculate_bartlett_sphericity, calculate_kmo, FactorAnalyzer
from sklearn.preprocessing import StandardScaler

df_city = pd.read_csv("data/CityDevelopment.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    print("Cleaning data for a df")
    if df.isna().any().any():
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_city_clean = cleanData(df_city)
numeric_cols = df_city_clean.columns[1:]
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_city_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index = df_city_clean.index,
    columns=numeric_cols
)
print(df_date_standardizate.head())

modelFA = FactorAnalyzer(n_factors=len(numeric_cols), rotation="varimax")
F = modelFA.fit(df_date_standardizate)

# Scoruri factoriale
eticheteFA = ["F" + str(i+1) for i in range(len(numeric_cols))]
scoruri = modelFA.transform(df_date_standardizate)
df_scoruri = pd.DataFrame(
    scoruri,
    index=df_date_standardizate.index,
    columns=eticheteFA
)
print(df_scoruri.head())

plt.figure()
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.title("Scoruri factoriale")
plt.show()

bartlettTest = calculate_bartlett_sphericity(df_date_standardizate)
print("Testul bartlett: ", bartlettTest)

kmoTest = calculate_kmo(df_date_standardizate)
print("KMO test: ", kmoTest)

var = modelFA.get_factor_variance()[0]
print("Variance: ", var)

corelatii = modelFA.loadings_
df_corelatii = pd.DataFrame(
    corelatii,
    index=numeric_cols,
    columns=eticheteFA
)
plt.figure()
sb.heatmap(df_corelatii)
plt.title("Corelograma")
plt.show()

comunalitati = modelFA.get_communalities()
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=["Comunalitati"]
)
plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Corelograma")
plt.show()