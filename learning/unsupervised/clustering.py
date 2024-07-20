from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd


def elbow_method(data, max_clusters=10):
    inertia_values = []
    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, random_state=42)
        kmeans.fit(data)
        inertia_values.append(kmeans.inertia_)

    plt.plot(range(2, max_clusters + 1), inertia_values, marker='o')
    plt.title('Metodo del gomito')
    plt.xlabel('Numero di cluster')
    plt.ylabel('Inerzia')
    plt.show()


df = pd.read_csv("../../dataset/encoded-playstore-apps.csv", na_filter=False)
elbow_method(df)