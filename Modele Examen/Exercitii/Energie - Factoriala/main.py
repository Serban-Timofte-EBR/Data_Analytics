import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo

# Calculați coeficientul de variație pentru fiecare variabilă numerică (raportul dintre abaterea standard și medie).
# Salvați rezultatele într-un fișier numit CoefficientOfVariation.csv.

df_economic = pd.read_csv("data/EconomicData.csv", index_col=0)
numeric_cols = df_economic.columns[0:]
print("Coloanele numerice: ", numeric_cols)

coeff_var = df_economic.std() / df_economic.mean()
df_cerinta1 = pd.DataFrame(
    coeff_var,
    index=numeric_cols,
    columns=["Coeficientul de variatie"]
)
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# eterminați țara cu cel mai mare consum de energie pe cap de locuitor (calculat ca EnergyConsumption împărțit la populație).
# Salvați rezultatul în TopEnergyConsumer.csv

df_economic["EnergyConsumptionPerCapita"] = df_economic["EnergyConsumption"] / df_economic["Population"]
df_cerinta2 = df_economic.sort_values(by="EnergyConsumptionPerCapita", ascending=False).head(1)
df_cerinta2.to_csv("data/results/Cerinta2.csv")

# Partea B - Analiza factoriala

df_economic = pd.read_csv("data/EconomicData.csv", index_col=0)

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
numeric_cols = df_economic_clean.columns[0:-3]
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_economic_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_economic_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/B_DateStandardizate.csv")

nrVar = len(numeric_cols)
modelAF = FactorAnalyzer(n_factors=nrVar, rotation="varimax")
F = modelAF.fit(df_date_standardizate)

scoruri = modelAF.transform(df_date_standardizate)
eticheteFA = ["F" + str(i+1) for i in range(nrVar)]
df_scoruri = pd.DataFrame(
    scoruri,
    index=df_date_standardizate.index,
    columns=eticheteFA
)
df_scoruri.to_csv("data/results/B_ScoruriFactoriale.csv")
print("Scoruri:")
print(df_scoruri)

plt.figure()
plt.scatter(df_scoruri["F1"], df_scoruri["F2"])
plt.title("Scatter F1 si F2")
plt.show()

bartlettScore =  calculate_bartlett_sphericity(df_date_standardizate)
print("Bartlett Score: ", bartlettScore[1])

kmoScore = calculate_kmo(df_date_standardizate)
print("KMO Score: ", kmoScore[1])

variance = modelAF.get_factor_variance()
print("Variatia: ", variance)

corelatii = modelAF.loadings_
df_corelatii = pd.DataFrame(
    corelatii,
    index=numeric_cols,
    columns=eticheteFA
)
print("Corelatiile:")
print(df_corelatii)

plt.figure()
sb.heatmap(df_corelatii)
plt.title("Heatmap Corelatii Factoriale")
plt.show()

comunalitati = modelAF.get_communalities()
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=["Comunalitati"]
)

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Heatmap Comunalitati")
plt.show()