import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Să se determine țările unde rata de șomaj (UnemploymentRate) este mai mare decât rata de creștere economică (GDPGrowth).

df_economic = pd.read_csv("data/EconomicDemographicData.csv",index_col=0)
df_continente = pd.read_csv("data/ContinentData.csv", index_col=0)

df_cerinta1 = df_economic[df_economic["UnemploymentRate"] > df_economic["GDPGrowth"]]
df_cerinta1 = df_cerinta1[["UnemploymentRate", "GDPGrowth"]]
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Să se identifice continentul cu cel mai mare PIB total (GDP) și să se salveze rezultatele într-un fișier numit TopGDPContinent.csv, cu următoarele coloane:
df_merge = df_economic.merge(
    df_continente,
    left_index=True,
    right_index=True
)
df_merge.to_csv("data/helpers/1_Merge.csv")

df_grouped = df_merge.groupby("Continent").sum().sort_values(by="GDP", ascending=False)
df_grouped.to_csv("data/helpers/2_Grouped.csv")

df_cerinta2 = df_grouped.head(1)
df_cerinta2.to_csv("data/results/Cerinta2.csv")

# Cerinta B - ACP
df_economic = pd.read_csv("data/EconomicDemographicData.csv", index_col=0)

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
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_economic_clean[numeric_cols])
df_data_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_economic_clean.index,
    columns=numeric_cols
)
df_data_standardizate.to_csv("data/results/B_1_DateStandardizate.csv")

modelACP = PCA()
C = modelACP.fit_transform(df_data_standardizate)

variance = modelACP.explained_variance_ratio_
cumVar = np.cumsum(variance)
print("Variance: ", variance)
print("Cum var: ", cumVar)

plt.figure()
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cumVar) + 1), cumVar)
plt.title("Graficul reprezentatitivitatii componentelor principale")
plt.show()

eticheteACP = ["C" + str(i+1) for i in range(len(variance))]
df_PCA = pd.DataFrame(
    C,
    index=df_economic_clean.index,
    columns=eticheteACP
)
df_PCA.to_csv("data/results/B_2_PCA.csv")

plt.figure()
plt.scatter(df_PCA["C1"], df_PCA["C2"])
plt.title("Scatter C1 si C2")
plt.xlabel("C1")
plt.ylabel("C2")
plt.show()

matricea_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
df_matrice = pd.DataFrame(
    matricea_corelatie,
    index=numeric_cols,
    columns=eticheteACP
)
df_matrice.to_csv("data/results/B_3_MatriceCorelatie.csv")

plt.figure()
sb.heatmap(df_matrice)
plt.title("Corelograma")
plt.show()

comunalitati = np.cumsum(matricea_corelatie**2, axis=1)
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=eticheteACP
)
df_comunalitati.to_csv("data/results/B_4_Comunalitati.csv")

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Corelograma Comunalitati")
plt.show()
