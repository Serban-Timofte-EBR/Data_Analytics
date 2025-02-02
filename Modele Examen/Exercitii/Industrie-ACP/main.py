import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Să se calculeze cifra de afaceri totală și cifra de afaceri pe locuitor pentru fiecare județ.
# Rezultatele vor fi salvate într-un fișier numit Cerinta1.csv, care va avea următoarele coloane:

df_industrie = pd.read_csv("data/Industrie.csv", index_col=0)
df_populatie = pd.read_csv("data/PopulatieJudet.csv", index_col=0)

numeric_cols_1 = df_industrie.columns[0:]
print("Coloanele numerice: ", numeric_cols_1)

df_merge = df_industrie.merge(
    df_populatie,
    left_index=True,
    right_index=True
)
df_merge.to_csv("data/helpers/1_Merge.csv")

df_merge["CifraDeAfaceriTotala"] = df_merge[numeric_cols_1].sum(axis = 1)
df_merge["CifraDeAfaceriPerCapita"] = df_merge["CifraDeAfaceriTotala"] / df_merge["Populatie"]

df_cerinta1 = df_merge[["CifraDeAfaceriTotala", "CifraDeAfaceriPerCapita"]]
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Să se determine activitatea industrială dominantă (cu cifra de afaceri cea mai mare) la nivel național. R
# Rezultatele vor fi salvate într-un fișier numit Cerinta2.csv, care va conține:

activitateMax = df_merge.drop(columns=["CifraDeAfaceriTotala", "CifraDeAfaceriPerCapita"]).idxmax(axis=1)

cerinta2_rows = []
for judet, activitate in activitateMax.items():
    valoareMaxima = df_merge.loc[judet, activitate]

    cerinta2_rows.append({
        "Judet": judet,
        "Activitate": activitate,
        "Valoarea Maxima": valoareMaxima
    })

df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/Cerinta2.csv", index=False)

# Cerinta B - Analiza ACP

df_dataset34 = pd.read_csv("data/DataSet_34.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ....")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_dataset34_clean = cleanData(df_dataset34)
df_dataset34_clean.to_csv("data/helpers/2_Clean.csv")

numeric_cols = df_dataset34_clean.columns[0:]
print("Coloane numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_dataset34_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_dataset34_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/Industrie_Standardizat.csv")

modelACP = PCA()
C = modelACP.fit_transform(df_date_standardizate)

variance = modelACP.explained_variance_ratio_
cumVar = np.cumsum(variance)

print("Variance: ", variance)
print("Cum var: ", cumVar)

plt.figure()
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cumVar) + 1), cumVar)
plt.title("Gradul de acoperire a componentelor principale")
plt.show()

etichetePCA = ["C" + str(i+1) for i in range(len(variance))]
df_variance = pd.DataFrame(
    variance,
    index=etichetePCA,
    columns=["Variatia"]
)
df_variance.to_csv("data/results/Variance.csv")


df_PCA = pd.DataFrame(
    C,
    index=df_date_standardizate.index,
    columns=etichetePCA
)
print("Dataframe PCA:")
print(df_PCA)

plt.figure()
plt.scatter(df_PCA["C1"], df_PCA["C2"])
plt.title("Scatter Componente principale")
plt.xlabel("Componenta 1")
plt.ylabel("Componenta 2")
plt.show()

matricea_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
print("Matricea de corelatie:")
df_matrice_corelatie = pd.DataFrame(
    matricea_corelatie,
    index=numeric_cols,
    columns=etichetePCA
)
print(df_matrice_corelatie)

plt.figure()
sb.heatmap(df_matrice_corelatie)
plt.title("Corelograma")
plt.show()

comunalitati = np.cumsum(matricea_corelatie**2, axis=1)
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=etichetePCA
)
print("Comunalitati:")
print(df_comunalitati)

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Corelograma")
plt.show()