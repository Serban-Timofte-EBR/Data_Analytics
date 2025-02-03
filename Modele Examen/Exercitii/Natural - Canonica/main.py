import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler

df_resources = pd.read_csv("data/NaturalResources.csv", index_col=0)

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

df_resources_clean = cleanData(df_resources)

set_productie = ["OilProduction", "GasProduction", "ElectricityProduction", "CoalProduction"]
set_consum = ["OilConsumption", "GasConsumption", "ElectricityConsumption", "CoalConsumption"]
numeric_cols = set_productie + set_consum

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_resources_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_resources_clean.index,
    columns=numeric_cols
)

X = df_date_standardizate[set_productie]
Y = df_date_standardizate[set_consum]

X, Y = X.align(Y, join="inner", axis=0)

modelCCA = CCA()
X_C, Y_C = modelCCA.fit_transform(X, Y)

# Scorurile
df_X_C = pd.DataFrame(
    X_C,
    index=X.index,
    columns=["X_C1", "X_C2"]
)
print("Scorurile canonice X:")
print(df_X_C)

df_Y_C = pd.DataFrame(
    Y_C,
    index=Y.index,
    columns=["Y_C1", "Y_C2"]
)
print("Scorurile canonice Y:")
print(df_Y_C)

corelatii = modelCCA.score(X, Y)
print("Corelatii: ", corelatii)

plt.figure()
plt.scatter(X_C[:, 0], X_C[:, 1], label="Productie")
plt.scatter(Y_C[:, 0], Y_C[:, 1], label="Consum")
plt.title("Scatter Canonic")
plt.show()

corr_X = np.corrcoef(X.T, X_C.T)[:X.shape[1], X.shape[1]:]
corr_Y = np.corrcoef(Y.T, Y_C.T)[:Y.shape[1], Y.shape[1]:]

plt.figure()
sb.heatmap(corr_X)
plt.title("Heapmap X")
plt.show()

plt.figure()
sb.heatmap(corr_Y)
plt.title("Heapmap Y")
plt.show()