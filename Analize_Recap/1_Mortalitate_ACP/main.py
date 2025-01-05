import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


df_mortalitate = pd.read_csv("data/Mortalitate.csv", index_col=0)
df_coduri = pd.read_csv("data/CoduriTariExtins.csv", index_col=0)

print("Dataframeuri din csv:")
print("Mortalitate:")
print(df_mortalitate)

print("Coduri:")
print(df_coduri)

def clean_data(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Curatarea datelor pentru dataframe")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_mortalitate = clean_data(df_mortalitate)
df_coduri = clean_data(df_coduri)

print("Dataframeuri curatate:")
print("Mortalitate:")
print(df_mortalitate)

print("Coduri:")
print(df_coduri)

df_merged = df_mortalitate.merge(
    df_coduri,
    right_index=True,
    left_index=True
)
print("Dataframe merge:")
print(df_merged)
df_merged.to_csv("data/inter/MergedDF.csv")

numeric_values = df_merged.select_dtypes(include=['float64', 'int64'])
scaler = StandardScaler()
date_standardizate = scaler.fit_transform(numeric_values)

print("Data standardizate:")
print(date_standardizate)

modelACP = PCA()
C = modelACP.fit_transform(date_standardizate)

variance = modelACP.explained_variance_ratio_
print("Varianta:")
print(variance)

etichete = ['C' + str(i+1) for i in range(len(variance))]
df_componente_principale = pd.DataFrame(
    data = C,
    index = df_merged.index,
    columns=etichete
)
print("Dataframe varianta componente principale:")
print(df_componente_principale)

plt.figure("Clustere componente principale")
plt.scatter(df_componente_principale['C1'], df_componente_principale['C2'])
plt.xlabel('C1')
plt.ylabel('C2')
plt.title("Scatter plot cu C1 si C2")
plt.show()

matrice_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_values.columns), len(numeric_values.columns):]
df_corelatie = pd.DataFrame(
    data=matrice_corelatie,
    index=numeric_values.columns,
    columns=etichete
)
print("Dataframe matrice de corelatie:")
print(df_corelatie)

plt.figure("Heatmap pentru matricea de corelatie")
sb.heatmap(df_corelatie)
plt.title("Corelograma")
plt.show()

comunalitati = np.cumsum(matrice_corelatie ** 2, axis = 1)
df_comunalitati = pd.DataFrame(
    data=comunalitati,
    index=numeric_values.columns,
    columns=etichete
)
print("Dataframe comunalitati:")
print(df_comunalitati)

plt.figure("Heatmap comunalitati")
sb.heatmap(df_comunalitati)
plt.title("Heatmap comunalitati")
plt.show()
