import warnings

from scipy.signal.windows import bartlett

warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo
from sklearn.preprocessing import StandardScaler

df_global = pd.read_csv("data/GlobalDevelopment.csv", index_col=0)
df_regions = pd.read_csv("data/RegionData.csv", index_col=0)

# Determinați țările cu cel mai mare și cel mai mic PIB
# (GDP_per_Capita * Population) și salvați rezultatele într-un fișier GDPExtremes.csv.

df_merge = df_global.merge(
    df_regions,
    left_index=True,
    right_index=True
)
df_merge["GDP"] = df_merge["GDP_per_Capita"] * df_merge["Population"]
df_merge = df_merge.sort_values(by="GDP", ascending=True)
df_merge.to_csv("data/helpers/1_Merge.csv")

df_cerinta1 = df_merge.head(1)
df_cerinta1.to_csv("data/results/A/Cerinta1.csv")

# Calculați rata medie a mortalității infantile pe continent și salvați rezultatele într-un fișier

df_grouped = df_merge.groupby("Continent")["InfantMortalityRate"].mean()
df_grouped.to_csv("data/results/A/Cerinta2.csv")

# B - Analiza Factoriala
df_global = pd.read_csv("data/GlobalDevelopment.csv", index_col=0)

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

df_global_clean = cleanData(df_global)
numeric_cols = df_global_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_global_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_global_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/B/1_DateStandardizate.csv")

nrVar = len(numeric_cols)
modelFA = FactorAnalyzer(n_factors=nrVar, rotation="varimax")
F = modelFA.fit(df_date_standardizate)

scoruri = modelFA.transform(df_date_standardizate)
eticheteFA = ["F" + str(i+1) for i in range(nrVar)]
print("Scoruri:")
df_scoruri = pd.DataFrame(
    scoruri,
    index=df_date_standardizate.index,
    columns=eticheteFA
)
df_scoruri.to_csv("data/results/B/2_ScoruriFactoriale.csv")
print(df_scoruri)

plt.figure()
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.title("Scatter componente principale")
plt.xlabel("F1")
plt.ylabel("F2")
plt.show()

bartlettScore = calculate_bartlett_sphericity(df_date_standardizate)
print("Scor Bartlett: ", bartlettScore[1])

kmoScore = calculate_kmo(df_date_standardizate)
print("Scor KMO: ", kmoScore[1])

variance = modelFA.get_factor_variance()
print("Variance: ", variance)

# Corelatii factoriale
corelatii = modelFA.loadings_
df_corelatii = pd.DataFrame(
    corelatii,
    index=numeric_cols,
    columns=eticheteFA
)
print("Corelatii:")
print(df_corelatii)

plt.figure()
sb.heatmap(df_corelatii)
plt.title("Corelatii factoriale")
plt.show()

comunalitati = modelFA.get_communalities()
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=["Comunalitati"]
)
print("Comunalitati:")
print(df_comunalitati)

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Comunalitati")
plt.show()