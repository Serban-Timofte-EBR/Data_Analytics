import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# 1. Citirea datelor din csv
df_alcohol = pd.read_csv("data/alcohol.csv", index_col=0)

print("Datele din csv - Alcohol.csv:")
print(df_alcohol)

# 2. Curatarea datelor

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data:")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_alcohol = cleanData(df_alcohol)

print("Datele curatate:")
print(df_alcohol)
df_alcohol.to_csv("data/1_clean/CleanData.csv")

# 3. Standardizare
lista_coloane_numerice = list(df_alcohol.columns[1:])
print("Lista coloanelor numerice:")
print(lista_coloane_numerice)

df_alcohol_date_numerice = df_alcohol[lista_coloane_numerice]
print("Dataframe date numerice:")
print(df_alcohol_date_numerice)

# df_numeric = df_alcohol.select_dtypes(include=['float64', 'int64'])
# print("df2")
# print(df_numeric)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_alcohol_date_numerice)
print("Datele standardizate:")
print(date_standardizate)

df_data_standardizate = pd.DataFrame(
    data=date_standardizate,
    index=df_alcohol.index,
    columns=lista_coloane_numerice
)
print("Dataframe standardizat:")
print(df_data_standardizate)
df_data_standardizate.to_csv("data/2_standardizat/DateStandardizate.csv")

# 4. Crearea dendogramei
def create_dendogram(df_date_standardizate):
    methods = ['single', 'average', 'ward', 'complete']
    linkage_matrices = {}

    for i, method in enumerate(methods, 1):
        plt.figure("Ierarhizarea de clusteri")

        # Ierarhizarea de clusteri
        linkage_matrix = linkage(df_data_standardizate, method = method)
        linkage_matrices[method] = linkage_matrix
        dendrogram(
            linkage_matrix,
            truncate_mode = 'lastp',
            p = 10
        )
        plt.title("Denograma de clusteri")
        plt.xlabel('Sample data')
        plt.ylabel('Distanta')
        plt.show()
    return linkage_matrices

# Salvam si matricea pentru urmatorii pasi
linkage_matrices = create_dendogram(df_data_standardizate)

# 5. Determinam numarul optim de clustere pentru analiza ward
linkage_matrix_ward = linkage_matrices['ward']
distance = linkage_matrix_ward[:, 2]
diference = np.diff(distance, 2)
punctul_elb = np.argmax(diference) + 1
print("Numarul optim de clustere este: ", punctul_elb)

# 6. Partitionarea datelor
clusters = fcluster(linkage_matrix_ward, t = punctul_elb, criterion='maxclust')

df_alcohol['Clusters'] = clusters
print("Datele cu clusterele atribuite:")
print(df_alcohol)
df_alcohol.to_csv("data/3_partition/PartionData.csv")

# 7. Validarea clusterizerii
silhouetteAvg = silhouette_score(df_data_standardizate, clusters)
print("Scorul silhouette: ", silhouetteAvg) # Scorul Silhouette foarte mic, cum ar fi 0.0139, indică o problemă de separare a clusterelor. Practic, clusterele identificate nu sunt bine definite sau există o suprapunere semnificativă între ele

# 8. Vizualizarea clusterelor în spațiul PCA
modelPCA = PCA()
C = modelPCA.fit_transform(df_data_standardizate)

# Varianta
variance = modelPCA.explained_variance_ratio_
print("Variance: ", variance)

etichetePCA = ['C' + str(i+1) for i in range(len(lista_coloane_numerice))]
df_pca = pd.DataFrame(
    data=C,
    index=df_alcohol.index,
    columns=etichetePCA
)
print("Dataframe PCA:")
print(df_pca)

plt.figure("Scatter pentru PCA")
plt.scatter(df_pca["C1"], df_pca["C2"])
plt.title("Scatter")
plt.xlabel("C1")
plt.ylabel("C2")
plt.show()

matice_corelatii = np.corrcoef(df_data_standardizate.T, C.T)[:len(lista_coloane_numerice), len(lista_coloane_numerice):]
df_corelatii = pd.DataFrame(
    data = matice_corelatii,
    index = df_alcohol_date_numerice.columns,
    columns=etichetePCA
)
print("Maticea de corelatie:")
print(matice_corelatii)

plt.figure("Heatmap corelatii")
sb.heatmap(df_corelatii, color = 'y')
plt.title("Heatmap matrice corelatii")
plt.show()

comunalitati = np.cumsum(matice_corelatii ** 2, axis = 1)
df_columalitati = pd.DataFrame(
    data = comunalitati,
    index = df_alcohol_date_numerice.columns,
    columns=etichetePCA
)

plt.figure("Heatmap comunalitati")
sb.heatmap(df_columalitati, color = 'y')
plt.title("Heatmap matrice comunalitati")
plt.show()



