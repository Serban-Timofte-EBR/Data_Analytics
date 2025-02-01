import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy.ndimage import label
from sklearn.cross_decomposition import CCA

df_emissions = pd.read_csv("data/Emissions.csv", index_col=0)
df_populatie_europa = pd.read_csv("data/PopulatieEuropa.csv", index_col=0)

# Partea A

# Cerinta 1
cols_tone = ["AirEmiss", "Sulphur", "Nitrogen", "Ammonia", "NonMeth", "Partic"]
cols_thousands = ["GreenGE", "GreenGIE"]
numeric_cols_emissions = cols_tone + cols_thousands
print("Numeric cols: ", numeric_cols_emissions)

df_emissions[cols_thousands] = df_emissions[cols_thousands] * 1000
df_emissions["Emisii_total_tone"] = df_emissions[cols_tone + cols_thousands].sum(axis=1)

# Selectăm coloanele necesare și salvăm rezultatele
df_cerinta1 = df_emissions[["Country", "Emisii_total_tone"]]
df_cerinta1.to_csv("data/results/cerinta1.csv")

# Cerinta 2
df_merged = df_emissions.merge(
    df_populatie_europa,
    left_index=True,
    right_index=True
).drop(columns=["Country_y"])
df_merged.to_csv("data/helpers/1_EmissionsRegions.csv")

df_regions = df_merged.groupby("Region").sum().drop(columns=["Country_x", "Emisii_total_tone"])
df_regions.to_csv("data/helpers/2_EmissionsGroupedByRegion.csv")

for col in numeric_cols_emissions:
    df_regions[col] = df_regions[col] / (df_regions["Population"] / 10000)

df_regions.drop(columns=["Population"]).to_csv("data/results/cerinta2.csv")

# B analiza canonica

df_emissions_2 = pd.read_csv("data/Emissions.csv")
df_electricity = pd.read_csv("data/ElectricityProduction.csv")

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

df_emissions_clean = cleanData(df_emissions_2)
df_electricity_clean = cleanData(df_electricity)

set_electricity = df_electricity_clean.columns[2:]
set_emissions = df_emissions_clean.columns[2:]

print("Set electricity: ", set_electricity)
print("Set emissions: ", set_emissions)

X = df_electricity_clean[set_electricity]
Y = df_emissions_clean[set_emissions]

X, Y = X.align(Y, join="inner", axis = 0)

# Modelul CCA
modelCCA =CCA()
X_c, Y_c = modelCCA.fit_transform(X, Y)

# Scorurile
df_X_c = pd.DataFrame(
    X_c,
    index=X.index,
    columns=["X_c1", "X_c2"]
)

df_Y_c = pd.DataFrame(
    Y_c,
    index=Y.index,
    columns=["Y_c1", "Y_c2"]
)

df_X_c.to_csv("data/results/z.csv", index=False)
df_Y_c.to_csv("data/results/u.csv", index=False)

# Corelatia
corelatia = modelCCA.score(X, Y)
with open("data/results/r.csv", "w") as file:
    file.write(str(corelatia))

# Vizualizarea
plt.figure("Vizualizarea componentelor")
plt.scatter(X_c[:, 0], X_c[:, 1], label = "Electricitate")
plt.scatter(Y_c[:, 0], Y_c[:, 1], label = "Emissions")
plt.title("Vizualizarea componentelor")
plt.show()

# Corelograma
corr_x = np.corrcoef(X.T, X_c.T)[:X.shape[1], X.shape[1]:]
corr_y = np.corrcoef(Y.T, Y_c.T)[:Y.shape[1], Y.shape[1]:]

df_corrX = pd.DataFrame(
    corr_x,
    index=set_electricity,
    columns=["X_c1", "X_c2"]
)

df_corrY = pd.DataFrame(
    corr_y,
    index=set_emissions,
    columns=["Y_c1", "Y_c2"]
)

plt.figure("Corelograma")
sb.heatmap(df_corrX)
plt.title("Corelograma")
plt.show()

plt.figure("Corelograma")
sb.heatmap(df_corrY)
plt.title("Corelograma")
plt.show()


