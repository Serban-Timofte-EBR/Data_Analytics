import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

from sklearn.preprocessing import StandardScaler, scale

df_gdp = pd.read_csv("data/GDP.csv", index_col=0)
df_corruption = pd.read_csv("data/corruption.csv", index_col=0)

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

df_gdp = cleanData(df_gdp)
df_corruption = cleanData(df_corruption)

df_dataset = df_gdp.merge(
    df_corruption,
    left_index=True,
    right_index=True
)
print("Dataset:")
print(df_dataset)

df_dataset_numeric = df_dataset.select_dtypes(include=['float64', 'int64'])
list_coloane_numerice = list(df_dataset_numeric.columns)

print("Lista coloanelor numerice: ", list_coloane_numerice)
print("Dataset numeric:")
print(df_dataset_numeric)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_dataset_numeric)

df_dataset_standardizat = pd.DataFrame(
    data=date_standardizate,
    index=df_dataset_numeric.index,
    columns=list_coloane_numerice
)
print("Dataset standardizat:")
print(df_dataset_standardizat)
df_dataset_standardizat.to_csv("data/StandardizedDataset.csv")

def create_dendrogram(df_date):
    methods = ['single', 'complete', 'average', 'ward']
    linkage_matrices = {}

    for i, method in enumerate(methods, 1):
        plt.figure("Denodrograma")

        linkage_matrix = linkage(df_date, method=method)
        linkage_matrices[method] = linkage_matrix
        dendrogram(
            linkage_matrix,
            truncate_mode="lastp",
            p = 10
        )

        plt.title("Dendrogram for " + method)
        plt.show()
    return linkage_matrices

linkage_matrices = create_dendrogram(df_dataset_standardizat)
linkage_matrix_ward = linkage_matrices["ward"]

differences = linkage_matrix_ward[:, :2]
distance = np.diff(differences, 2)
punct_elb = np.argmax(differences) + 1
print("Numarul de clustere optim: ", punct_elb)

clusters = fcluster(linkage_matrix_ward, criterion='maxclust', t=punct_elb)
df_dataset_numeric['Clusters'] = clusters
print("Dataset cu clustere:")
print(df_dataset_numeric)

# silhouetteScore = silhouette_score(df_dataset_standardizat, clusters)
# print("Silhouetter score: ", silhouetteScore)

modelACP = PCA()
C = modelACP.fit_transform(df_dataset_standardizat)

eticheteACP = ['C' + str(i+1) for i in range(C.shape[1])]
df_dataset_acp = pd.DataFrame(
    data=C,
    index=df_dataset_standardizat.index,
    columns=eticheteACP
)
print("Dataframe ACP:")
print(df_dataset_acp)

variance = modelACP.explained_variance_ratio_
print("Variance: ", variance)

plt.figure("Scatter ACP")
plt.scatter(df_dataset_acp["C1"], df_dataset_acp["C2"])
plt.xlabel("C1")
plt.ylabel("C2")
plt.title("Scatter ACP")
plt.show()

matrice_corelatii = np.corrcoef(df_dataset_standardizat.T, C.T)[:len(list_coloane_numerice), len(list_coloane_numerice):]
df_matrice_corelatie = pd.DataFrame(
    data=matrice_corelatii,
    index=list_coloane_numerice,
    columns=eticheteACP
)
print("Matricea de corelatie:")
print(df_matrice_corelatie)

plt.figure("heatmap corelatii")
sb.heatmap(df_matrice_corelatie)
plt.title("Heatmap corelatii")
plt.show()

cumunalitati = np.cumsum(matrice_corelatii ** 2, axis=1)
df_cumunalitati = pd.DataFrame(
    data=cumunalitati,
    index=list_coloane_numerice,
    columns=eticheteACP
)
plt.figure("heatmap cumunalitati")
sb.heatmap(df_cumunalitati)
plt.title("Heatmap cumunalitati")
plt.show()