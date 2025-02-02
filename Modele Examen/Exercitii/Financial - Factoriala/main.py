import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo
from sklearn.preprocessing import StandardScaler

df_financial = pd.read_csv("data/FinancialMarkets.csv", index_col=0)
df_regions = pd.read_csv("data/RegionCodes.csv", index_col=0)

# Cerinta 1:
# Să se determine țările în care rata dobânzii (InterestRate) este mai mică decât rata inflației (InflationRate).
# Rezultatele să fie salvate într-un fișier numit InterestVsInflation.csv, cu următoarele coloane:
# 	•	Country: Numele țării
# 	•	InterestRate: Rata dobânzii
# 	•	InflationRate: Rata inflației

df_filtred = df_financial[df_financial["InterestRate"] < df_financial["InflationRate"]]
df_cerinta1 = df_filtred[["InterestRate", "InflationRate"]]
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Cerinta 2:
# Să se calculeze PIB-ul mediu pe regiuni și să se salveze rezultatele în fișierul RegionGDP.csv.
# Structura fișierului:
# 	•	Region: Numele regiunii
# 	•	GDP_Average: PIB-ul mediu

df_merged = df_financial.merge(
    df_regions,
    left_index=True,
    right_index=True
)
df_merged.to_csv("data/helpers/1_Merge.csv")

df_grouped = df_merged.groupby("Region").mean()
df_grouped = df_grouped[["GDP"]].rename(columns={"GDP": "GDP_Average"})
df_grouped.to_csv("data/results/Cerinta2.csv")

# B - Analiza factoriala

df_financial_2 = pd.read_csv("data/FinancialMarkets.csv", index_col=0)

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

df_financial_clean = cleanData(df_financial_2)
numeric_cols = df_financial_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_financial_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index = df_financial_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/helpers/2_Standard.csv")

nrVar = len(numeric_cols)
modelFA = FactorAnalyzer(n_factors=nrVar, rotation="varimax")
F = modelFA.fit(df_date_standardizate)

scoruri = modelFA.transform(df_date_standardizate)
print("Scoruri: ")

eticheteFA = ["F" + str(i+1) for i in range(nrVar)]
df_scoruri = pd.DataFrame(
    scoruri,
    index=df_date_standardizate.index,
    columns=eticheteFA
)
print(df_scoruri)

plt.figure()
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.title("Scatter Factorial")
plt.show()

bartlettScore = calculate_bartlett_sphericity(df_date_standardizate)
print("Score Barlett: ", bartlettScore[1])

kmoScore = calculate_kmo(df_date_standardizate)
print("Score KMO: ", kmoScore[1])

variance = modelFA.get_factor_variance()
print("Variance: ", variance)

# Corelatii factoriale
corelatii = modelFA.loadings_
print("Corelatii:")

df_corelatii = pd.DataFrame(
    corelatii,
    index=numeric_cols,
    columns=eticheteFA
)
print(df_corelatii)

plt.figure()
sb.heatmap(df_corelatii)
plt.title("Heatmap corelatii")
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
plt.title("Heatmap comunalitati")
plt.show()