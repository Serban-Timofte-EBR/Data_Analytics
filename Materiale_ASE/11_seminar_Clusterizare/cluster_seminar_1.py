import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.preprocessing import StandardScaler

# load dataset
def load_iris_data():
    iris = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
        header=None,
        names=["sepal_length", "sepal_width", "petal_length", "petal_width", "species"],
    )

    X = iris.iloc[:, :-1].values
    species = iris.iloc[:, -1].values
    return X, species, iris

# pre procesare (standardizare)
def preprocess_data(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

# crearea dendogramei
def create_dendogram(X):
    methods = ['single', 'complete', 'average', 'ward'] # sunt metode de calculare ale dendogramei
                                                        # Complet = media distantei dintre toate punctele din cele doua clustere
                                                        # Single = distanta minima dintre toate punctele din cele doua clustere
                                                        # Average = media distantei dintre toate punctele din cele doua clustere
                                                        # Ward = distanta dintre toate punctele din cele doua clustere
    for i, method in enumerate(methods, 1):
        plt.figure(figsize=(20, 10))
        plt.subplot(2,2, i)

        # Ierarhizare cluster
        Z = linkage(X, method=method)
        dendrogram(
            Z,
            truncate_mode='lastp',  # afiseaza ultimele p cluster
            p=10,  # numarul maxim de cluster
            show_leaf_counts=True,
            leaf_rotation=90.,
            leaf_font_size=8.,
            show_contracted=True
        )
        plt.title(f'Diagrama de clusterizare ierarhica cu metoda: {method}')
        plt.xlabel('Sample index')
        plt.ylabel('Distanta')

    plt.tight_layout()
    plt.show()

# apelare functii
def main():
    X, species, iris = load_iris_data()
    X_scaled = preprocess_data(X)
    create_dendogram(X_scaled)

main()