import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df_indicatori = pd.read_csv("date/GlobalIndicatorsPerCapita_2021.csv", index_col=0)
df_coduri = pd.read_csv("date/CoduriTari.csv", index_col=0)

# A
# Cerinta 1
cols_valoarea_adaugata = df_indicatori.columns[8:]
print("Coloanele valoarea adaugata: ", cols_valoarea_adaugata)

df_indicatori["Valoare Adaugata"] = df_indicatori[cols_valoarea_adaugata].sum(axis=1)
df_cerinta1 = df_indicatori[["Country", "Valoare Adaugata"]]
df_cerinta1.to_csv("date/results/Cerinta1.csv")

# Cerinta 2
cols_coef_variatie = df_indicatori.columns[1:-1]
print("Coloane coef variatie: ", cols_coef_variatie)

df_merged = df_indicatori.merge(
    df_coduri,
    left_index=True,
    right_index=True
).drop(columns=["Country_y"])
df_merged.to_csv("date/helpers/1_Merge.csv")

df_grouped = df_merged.groupby("Continent").sum().drop(columns=["Country_x", "Valoare Adaugata"])
df_grouped.to_csv("date/helpers/2_Grouped.csv")

# B - ACP
df_indicatori_2 = pd.read_csv("date/GlobalIndicatorsPerCapita_2021.csv", index_col=0)

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

df_indicatori_clean = cleanData(df_indicatori_2)

numeric_cols = df_indicatori_clean.columns[1:]
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_indicatori_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_indicatori_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("date/helpers/3_Stand.csv")

modelACP = PCA()
C = modelACP.fit_transform(df_date_standardizate)
print(C)

variance = modelACP.explained_variance_ratio_
print("Variance: ", variance)

cumVar = np.cumsum(variance)
plt.figure("Grafic variatie")
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cumVar) + 1), cumVar)
plt.title("Grafic variatie")
plt.show()

etichetePCA = ["C" + str(i+1) for i in range(len(variance))]
df_PCA = pd.DataFrame(
    C,
    index=df_date_standardizate.index,
    columns=etichetePCA
)
df_PCA.to_csv("date/results/scoruri.csv")

plt.figure("Graficul PCA")
plt.scatter(df_PCA["C1"], df_PCA["C2"])
plt.title("Graficul PCA")
plt.show()

matrice_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
print("Matrice corelatie:")
print(matrice_corelatie)

plt.figure("Heatmap corelatie")
sb.heatmap(matrice_corelatie)
plt.title("Heatmpa corelatie")
plt.show()

comunalitati = np.cumsum(matrice_corelatie**2, axis=1)
print("Comunalitati: ", comunalitati)

plt.figure("Heatmap comunalitati")
sb.heatmap(comunalitati)
plt.title("Heatmpa comunalitati")
plt.show()
