import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo

df_economic = pd.read_csv("data/EconomicHealthData.csv", index_col=0)
df_continent = pd.read_csv("data/ContinentData.csv", index_col=0)

# Determinați suma totală a cheltuielilor pentru sănătate (HealthcareExpenditure) la nivel de continent, ținând cont de populația
# fiecărei țări. Calculați cheltuielile totale pentru sănătate ale fiecărei țări ca produs între HealthcareExpenditure și
# Population. Salvați rezultatele într-un fișier numit HealthcareByContinent.csv, care să includă următoarele coloane:

df_merge = df_economic.merge(
    df_continent,
    left_index=True,
    right_index=True
)
df_merge["TotalHealthcareExpenditure"] = df_merge["HealthcareExpenditure"] * df_merge["Population"]
df_merge.to_csv("data/helpers/1_Merge.csv")

df_grouped = df_merge.groupby("Continent").sum()
df_cerinta1 = df_grouped[["TotalHealthcareExpenditure"]]
df_cerinta1.to_csv("data/results/A/Cerinta1.csv")

# Calculați media speranței de viață (LifeExpectancy) și media ratei mortalității infantile (InfantMortalityRate)
# pentru fiecare continent.
df_grouped = df_merge.groupby("Continent").mean()
df_cerinta2 = df_grouped[["LifeExpectancy", "InfantMortalityRate"]]
df_cerinta2.to_csv("data/results/A/Cerinta2.csv")

# Cerinta B - Analiza factoriala
df_economic = pd.read_csv("data/Dataset.csv", index_col=0)

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
numeric_cols = df_economic_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_economic_clean[numeric_cols])
df_data_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_economic_clean.index,
    columns=numeric_cols
)
df_data_standardizate.to_csv("data/results/B/1_DataStandardizate.csv")

nrVar = len(numeric_cols)
modelFA = FactorAnalyzer(n_factors=nrVar, rotation=None)
F = modelFA.fit(df_data_standardizate)

scoruri = modelFA.transform(df_data_standardizate)
eticheteFA = ["F" + str(i+1) for i in range(nrVar)]
print("Scoruri:")
df_scoruri = pd.DataFrame(
    scoruri,
    index=df_data_standardizate.index,
    columns=eticheteFA
)
df_scoruri.to_csv("data/results/B/2_ScoruriFactoriale.csv")
print(df_scoruri)

bartlettScore = calculate_bartlett_sphericity(df_data_standardizate)
print("Score Bartlett: ", bartlettScore[1])

kmoScore = calculate_kmo(df_data_standardizate)
print("KMO Score: ", kmoScore[1])

plt.figure()
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.title("Scatter componente factoriale")
plt.xlabel("F1")
plt.ylabel("F2")
plt.show()

variance = modelFA.get_factor_variance()
df_variance = pd.DataFrame(
    variance,
    index=["Variance", "Proportion", "Cumulative"],
    columns=eticheteFA
)
df_variance.to_csv("data/results/B/3_Variance.csv")

corelatii = modelFA.loadings_
df_corelatii = pd.DataFrame(
    corelatii,
    index=numeric_cols,
    columns=eticheteFA
)
df_corelatii.to_csv("data/results/B/4_CorelatiiFactoriale.csv")

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
df_comunalitati.to_csv("data/results/B/5_Comunalitati.csv")

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Comunalitati")
plt.show()