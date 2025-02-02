import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler

df_health = pd.read_csv("data/HealthAndLifestyle.csv", index_col=0)
df_regions = pd.read_csv("data/RegionCodes.csv", index_col=0)

# Țările unde LifeExpectancy este mai mare de 80 de ani și ObesityRate este mai mică de 20%.
df_filtered = df_health[df_health["LifeExpectancy"] > 80]
df_filtered2 = df_filtered[df_filtered["ObesityRate"] < 20]
df_filtered2.to_csv("data/results/Cerinta1.csv")

# Statistici descriptive pe continente
df_merged = df_health.merge(
    df_regions,
    left_index=True,
    right_index=True
)
df_merged["Counter"]=1
df_merged.to_csv("data/helpers/1_Merge.csv")

df_groupedMean = df_merged.groupby("Region").mean()
df_groupedMean.to_csv("data/helpers/2_GroupedMean.csv")

df_groupedStd = df_merged.groupby("Region").std()
df_groupedStd.to_csv("data/helpers/2_GroupedStd.csv")

df_stats = pd.DataFrame({
    "HealthExpenditure_Mean": df_groupedMean["HealthExpenditure"],
    "HealthExpenditure_Std": df_groupedStd["HealthExpenditure"],
    "AlcoholConsumption_Mean": df_groupedMean["AlcoholConsumption"],
    "AlcoholConsumption_Std": df_groupedStd["AlcoholConsumption"]
})
df_stats.to_csv("data/results/Cerinta2.csv")

# Cerinta B - Analiza canonica

df_health = pd.read_csv("data/HealthAndLifestyle.csv", index_col=0)

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

df_health_clean = cleanData(df_health)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_health_clean)
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index = df_health_clean.index,
    columns=df_health_clean.columns
)

set_health = ["HealthExpenditure", "PhysiciansPer1000", "HospitalBedsPer1000"]
set_life = ["LifeExpectancy", "ObesityRate", "SmokingRate", "PhysicalActivityRate"]

X = df_date_standardizate[set_health]
Y = df_date_standardizate[set_life]

X, Y = X.align(Y, join="inner", axis=0)

modelCCA = CCA(n_components=2)
X_C, Y_C = modelCCA.fit_transform(X, Y)

df_XC = pd.DataFrame(
    X_C,
    index=X.index,
    columns=["X_C1", "X_C2"]
)

df_YC = pd.DataFrame(
    Y_C,
    index=Y.index,
    columns=["Y_C1", "Y_C2"]
)

df_XC.to_csv("data/results/X_ScoruriCanonice.csv")
df_YC.to_csv("data/results/Y_ScoruriCanonice.csv")

plt.figure()
plt.scatter(X_C[:, 0], X_C[:, 1], label = "Health")
plt.scatter(Y_C[:, 0], Y_C[:, 1], label = "Life")
plt.title("Primele doua radacini canonice")
plt.show()

# Corelatiile
corelatii = modelCCA.score(X, Y)
print("Corelatii: ", corelatii)

# Corelograma
corr_X = np.corrcoef(X.T, X_C.T)[:X.shape[1], X.shape[1]:]
corr_Y = np.corrcoef(Y.T, Y_C.T)[:Y.shape[1], Y.shape[1]:]

plt.figure()
sb.heatmap(corr_X)
plt.title("Corelograma X")
plt.show()

plt.figure()
sb.heatmap(corr_X)
plt.title("Corelograma Y")
plt.show()