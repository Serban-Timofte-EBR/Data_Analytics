import pandas as pd
import seaborn as sns

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score
from sklearn.cluster import KMeans


def pca(data, numeric_columns, output_path):
    standardize_data = data[numeric_columns]

    pca = PCA()
    principal_components = pca.fit_transform(standardize_data)

    explained_variance = pca.explained_variance_ratio_

    df_pca = pd.DataFrame(
        principal_components,
        columns=[f'PC{i + 1}' for i in range(principal_components.shape[1])]
    )

    df_pca.to_csv(output_path, index=False)

    plt.figure(figsize=(10, 6))
    plt.bar(range(1, len(explained_variance) + 1), explained_variance, alpha=0.7, align='center')
    plt.step(range(1, len(explained_variance) + 1), explained_variance.cumsum(), where='mid', color='red')
    plt.xlabel('Principal Components')
    plt.ylabel('Variance Explained')
    plt.title('PCA Explained Variance')
    plt.show()

    return df_pca, explained_variance

def kmeans_clustering(data, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(data)
    return clusters

def visualize(data, x_pc = 'PC1', y_pc = 'PC2', clusters = None):
    plt.figure(figsize=(8, 6))
    if clusters is not None:
        data['Cluster'] = clusters
        sns.scatterplot(
            x=data[x_pc], y=data[y_pc], hue=data['Cluster'], palette='viridis', s=60
        )
        plt.legend(title='Cluster')
    else:
        plt.scatter(data[x_pc], data[y_pc], alpha=0.7)
    plt.xlabel(x_pc)
    plt.ylabel(y_pc)
    plt.title('PCA Scatter Plot with Clusters' if clusters is not None else 'PCA Scatter Plot')
    plt.show()