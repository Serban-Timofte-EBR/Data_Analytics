import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df_demographic = pd.read_csv("data/DemographicData.csv", index_col=0)
df_regions = pd.read_csv("data/RegionCodes.csv", index_col=0)

# 1. Cerinta 1
# Să se calculeze suma populației și PIB-ul total pe regiune.
# Rezultatele să fie salvate într-un fișier numit RegionStatistics.csv.

df_merged = df_demographic.merge(
    df_regions,
    left_index=True,
    right_index=True
)
df_merged.to_csv("data/helpers/1_Merge.csv")

df_grouped = df_merged.groupby("Region").sum()
df_grouped.to_csv("data/helpers/2_Gruped.csv")

cerinta1_rows = []
for index, row in df_grouped.iterrows():
    cerinta1_rows.append({
        "Region": index,
        "PopulationSum": row["Population"],
        "GDP_Sum": row["GDP"]
    })
df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/results/RegionStatistics.csv", index=False)

# 2.	Cerinta 2
# Să se determine țara cu cea mai mare speranță de viață pentru fiecare regiune.
# Rezultatele să fie salvate într-un fișier numit TopLifeExpectancy.csv.
index_max_life = df_merged.groupby("Region")["LifeExpectancy"].idxmax()

cerinta2_rows = []
for region, country in index_max_life.items():
    lifeExpectacy = df_demographic.loc[country, "LifeExpectancy"]
    cerinta2_rows.append({
        "Region": region,
        "Country": country,
        "LifeExpectancy": lifeExpectacy
    })
df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/TopLifeExpectancy.csv", index=False)

# B - Analiza în Componente Principale (PCA)

df_demographic_2 = pd.read_csv("data/DemographicData.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ... ")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_demographic_clean = cleanData(df_demographic_2)
numeric_cols = df_demographic_clean.columns[0:]
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_demographic_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index = df_demographic_clean.index,
    columns=numeric_cols
)
print("Datele standardizate:")
print(df_date_standardizate)

modelACP = PCA()
C = modelACP.fit_transform(df_date_standardizate)

variance = modelACP.explained_variance_ratio_
print("Variance: ", variance)

eticheteACP = ["C" + str(i+1) for i in range(len(variance))]
df_pca = pd.DataFrame(
    C,
    index=df_demographic_clean.index,
    columns=eticheteACP
)
print(df_pca)

cumVariance = np.cumsum(variance)
plt.figure()
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cumVariance) + 1), cumVariance)
plt.title("Grafic variatie")
plt.show()

plt.figure()
plt.scatter(df_pca["C1"], df_pca["C2"])
plt.title("Scatter C1 si C2")
plt.xlabel("C1")
plt.ylabel("C2")
plt.show()

matrice_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
print("Matricea de corelatie:")
print(matrice_corelatie)

df_matrice_corelatie = pd.DataFrame(
    matrice_corelatie,
    index=numeric_cols,
    columns=eticheteACP
)

plt.figure()
sb.heatmap(df_matrice_corelatie)
plt.title("Heatmap Matrice Corelatie")
plt.show()

comunalitati = np.cumsum(matrice_corelatie ** 2, axis=1)
print("Comunalitati: ", comunalitati)

df_comunalitati = pd.DataFrame(
    comunalitati,
    index = numeric_cols,
    columns=eticheteACP
)
print(df_comunalitati)

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Heatmap Matrice Comunalitati")
plt.show()

cosinusuri = matrice_corelatie ** 2
print("Cosinusuri:")
df_cosinusuri = pd.DataFrame(
    cosinusuri,
    index=numeric_cols,
    columns=eticheteACP
)
print(df_cosinusuri)

contributii = matrice_corelatie ** 2 / np.sum(matrice_corelatie ** 2, axis=0)
df_contributii = pd.DataFrame(
    contributii,
    index=numeric_cols,
    columns=eticheteACP
)
print("Contributii:")
print(df_contributii)