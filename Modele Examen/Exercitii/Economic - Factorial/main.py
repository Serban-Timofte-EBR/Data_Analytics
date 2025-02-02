import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from factor_analyzer import FactorAnalyzer
from sklearn.preprocessing import StandardScaler

df_economics = pd.read_csv("data/EconomicData.csv", index_col=0)
df_coduri = pd.read_csv("data/ContinentCodes.csv", index_col=0)

# Să se determine PIB-ul total și rata medie a șomajului pentru fiecare continent.
# Rezultatele să fie salvate într-un fișier numit ContinentalStatistics.csv, cu următoarele coloane:

df_merged = df_economics.merge(
    df_coduri,
    left_index=True,
    right_index=True
)
df_merged.to_csv("data/helpers/1_Merge.csv")

df_continente_PIBTotal = df_merged.groupby("Continent").sum()
df_continente_SomajMediu = df_merged.groupby("Continent").mean()

df_cerinta1 = pd.DataFrame({
    "Total_GDP": df_continente_PIBTotal["GDP"],
    "Mean_UnemploymentRate": df_continente_SomajMediu["UnemploymentRate"]
})
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Să se determine indicatorul (GDP, UnemploymentRate, ExportRate, ImportRate, Population) care înregistrează valoarea maximă pentru fiecare continent.
# Rezultatele să fie salvate într-un fișier numit TopIndicators.csv, cu următoarele coloane:
cerinta2Items = df_continente_PIBTotal.idxmax()

cerinta2_rows = []
for indicator, continent in cerinta2Items.items():
    maxVal = df_continente_PIBTotal.loc[continent, indicator]

    cerinta2_rows.append({
        "Continent": continent,
        "Indicator": indicator,
        "MaxValue": maxVal
    })

df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/Cerinta2.csv", index=False)

# B - Analiza factoriala
df_economics_2 = pd.read_csv("data/EconomicData.csv", index_col=0)

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

df_economics_clean = cleanData(df_economics_2)
df_economics_clean.to_csv("data/helpers/2_Clean.csv")

numeric_cols = df_economics_clean.columns[0:]
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_economics_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_economics_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/helpers/3_Standard.csv")

nrVar = len(numeric_cols)
modelFA = FactorAnalyzer(n_factors=nrVar, rotation="varimax")
F = modelFA.fit(df_date_standardizate)

scoruri = modelFA.transform(df_date_standardizate)

eticheteFA = ["F" + str(i+1) for i in range(nrVar)]
df_FA = pd.DataFrame(
    scoruri,
    index=df_date_standardizate.index,
    columns=eticheteFA
)
print("DF Factorial:")
print(df_FA)

plt.figure()
plt.scatter(df_FA["F1"], df_FA["F2"])
plt.title("Scatter Factorial")
plt.show()

variance = modelFA.get_factor_variance()
print("Variance: ", variance)

corelatii = modelFA.loadings_
df_corelatii = pd.DataFrame(
    corelatii,
    index=numeric_cols,
    columns=eticheteFA
)
print("DF Corelatii:")
print(df_corelatii)

plt.figure()
sb.heatmap(df_corelatii)
plt.title("Corelograma factoriala")
plt.show()

comunalitati = modelFA.get_communalities()
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=["Comunalitati"]
)

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Corelograma Comunalitati")
plt.show()