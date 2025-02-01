# Analiza ACP completa

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# A

# Cerinta 1
df_mise = pd.read_csv("data/MiseNatPopTari.csv", index_col=0)
print("Head csv:")
print(df_mise.head())

numeric_cols = df_mise.columns[3:]
print("Coloanele numerice: ", numeric_cols)

cerinta1_rows = []
for index, row in df_mise.iterrows():
    average = row[numeric_cols].mean()

    cerinta1_rows.append({
        "CodTara": index,
        "NumeTara": row["Country_Name"],
        "Medie": average
    })

df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/results/cerinta1.csv", index=False)

# Cerinta 2

df_coduri = pd.read_csv("data/CoduriTariExtins.csv", index_col=0)
df_merged = df_mise.merge(
    df_coduri,
    left_index=True,
    right_index=True
).drop(columns=["Country_Name_y"])
df_merged.to_csv("data/helpers/1_DFMerged.csv")

df_grouped_by_continent = df_merged.groupby("Continent").sum().drop(columns=["Country_Name_x", "Three_Letter_Country_Code"])
df_grouped_by_continent.to_csv("data/helpers/2_DFGrouped.csv")

cerinta2_rows = []
for index, row in df_grouped_by_continent.iterrows():
    total = row[numeric_cols].sum()
    average = row[numeric_cols].mean()

    cerinta2_rows.append({
        "Continent": index,
        "Total": total,
        "Medie": average
    })

df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/cerinta2.csv", index=False)

# B - Analiza ACP completa

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

# Curatarea datelor
df_mise_clean = cleanData(df_mise)
df_coduri_clean = cleanData(df_coduri)
df_combined = df_mise.merge(df_coduri, right_index=True, left_index=True).drop(columns=["Country_Name_y"])
print("Dataframe pentru analiza ACP:")
print(df_combined.head())

# Standardizarea datelor
df_numeric = df_combined[numeric_cols]
print("Dataframe numeric:")
print(df_numeric.head())

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_numeric)
print("Datele standardizate:")
print(date_standardizate)

# Model ACP
modelACP = PCA()
C = modelACP.fit_transform(date_standardizate)

variance = modelACP.explained_variance_ratio_
print("Variatia: ", variance)

with open("data/results/variante_componente.csv", "w") as file:
    for i in range(len(variance)):
        file.write(str(variance[i]) + ", ")


# Plot varianță componente
cum_variance = np.cumsum(variance)
plt.figure("Variatia componentelor")
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cum_variance) + 1), cum_variance)
plt.title("Variatia componentelor")
# plt.show()

# Dataframe cu scorurile
eticheteACP = ["C" + str(i+1) for i in range(len(variance))]
df_scoruri = pd.DataFrame(
    C,
    index=df_numeric.index,
    columns=eticheteACP
)
print("Scorurile componentelor principale:")
print(df_scoruri)

plt.figure("Plot componente principale")
plt.scatter(df_scoruri["C1"], df_scoruri["C2"])
plt.xlabel("C1")
plt.ylabel("C2")
plt.title("Plot componente principale")
# plt.show()

# Corelatii factoriale
matricea_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
print("Matricea de corelatie:")
print(matricea_corelatie)

df_matrice_corelatie = pd.DataFrame(
    matricea_corelatie,
    index=numeric_cols,
    columns=eticheteACP
)
print("Dataframe corelatie:")
print(df_matrice_corelatie)

plt.figure("Corelograma factoriala")
sb.heatmap(df_matrice_corelatie)
plt.title("Corelograma factoriala")
# plt.show()

# Comunalitati
comunalitati = np.cumsum(matricea_corelatie ** 2, axis=1)
print("Comunalitati: ", comunalitati)
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=eticheteACP
)
print("Dataframe comunalitati:")
print(df_comunalitati)

plt.figure("Corelograma comunalitati")
sb.heatmap(df_comunalitati)
plt.title("Corelograma comunalitati")
# plt.show()

# Cosinusuri
cosinusuri = matricea_corelatie ** 2
df_cosinusuri = pd.DataFrame(
    cosinusuri,
    index=numeric_cols,
    columns=eticheteACP
)
print("Dataframe cosinusuri:")
print(df_cosinusuri)

# Contributii
contributii = matricea_corelatie ** 2 / np.sum(matricea_corelatie ** 2, axis = 0)
df_contributii = pd.DataFrame(
    contributii,
    index=numeric_cols,
    columns=eticheteACP
)
print("Dataframe contributii:")
print(df_contributii)