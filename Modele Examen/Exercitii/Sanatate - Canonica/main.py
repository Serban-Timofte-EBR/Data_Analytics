import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler

df_health = pd.read_csv("HealthData.csv", index_col=0)
df_economic = pd.read_csv("EconomicData.csv", index_col=0)

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
df_economic_clean = cleanData(df_economic)

scaler = StandardScaler()
health_stand = scaler.fit_transform(df_health_clean)
economics_stand = scaler.fit_transform(df_economic_clean)

df_health_stand = pd.DataFrame(
    health_stand,
    index=df_health_clean.index,
    columns=df_health_clean.columns
)

df_economic_stand = pd.DataFrame(
    economics_stand,
    index=df_economic_clean.index,
    columns=df_economic_clean.columns
)

variabile_sanatate = df_health_clean.columns[0:-1]
variabile_economice = df_economic_clean.columns[0:]
print("Variabile sanatate: ", variabile_sanatate)
print("Variabile economice: ", variabile_economice)

X = df_health_stand[variabile_sanatate]
Y = df_economic_stand[variabile_economice]

X, Y = X.align(Y, join="inner", axis=0)

modelCCA = CCA(n_components=2)
X_C, Y_C = modelCCA.fit_transform(X, Y)

# Scoruri
df_XC = pd.DataFrame(
    X_C,
    index=X.index,
    columns=["X_C1", "X_C2"]
)
df_XC.to_csv("1_ScoruriXC.csv")

df_YC = pd.DataFrame(
    Y_C,
    index=Y.index,
    columns=["Y_C1", "Y_C2"]
)
df_YC.to_csv("2_ScoruriYC.csv")

plt.figure()
plt.scatter(X_C[:, 0], X_C[:, 1])
plt.scatter(Y_C[:, 0], Y_C[:, 1])
plt.title("Scatter canonic")
plt.show()

# Corelatii
corr_X = np.corrcoef(X.T, X_C.T)[:X.shape[1], X.shape[1]:]
corr_Y = np.corrcoef(Y.T, Y_C.T)[:Y.shape[1], Y.shape[1]:]

plt.figure()
sb.heatmap(corr_X)
plt.title("Corelograma X")
plt.show()

plt.figure()
sb.heatmap(corr_Y)
plt.title("Corelograma Y")
plt.show()