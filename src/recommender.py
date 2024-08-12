import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from encoding import encode_dataset, encode_user_input


def similarity_with_cosine(row_a, row_b):
    element = cosine_similarity([row_a], [row_b])
    row_a["similarity"] = element[0][0]
    return row_a["similarity"]


def find_recommendations(app_name, category, rating, downloads, price, content_rating, editors_choice, success_rate):
    balanced_df = pd.read_csv("../dataset/balanced-playstore-apps.csv", na_filter=False)
    balanced_df = balanced_df.drop_duplicates(subset="App Id", keep="first")
    balanced_df = balanced_df[balanced_df["Category"] == category]
    balanced_df.reset_index(drop=True, inplace=True)
    balanced_df = balanced_df.drop(columns=["App Id", "Size (MB)", "Minimum Android", "Developer Id",
                                            "Last Updated", "Ad Supported", "In App Purchases", "Category"], axis=1)

    # Codifica dataset e input utente in valori numerici
    encoded_df, app_name_model = encode_dataset(balanced_df)

    user_input = [app_name, rating, downloads, price, content_rating, editors_choice, success_rate]
    encoded_user_input = encode_user_input(user_input, app_name_model)

    # Espansione colonne AppName di encoded_df
    app_name_expanded = pd.DataFrame(encoded_df["App Name"].tolist()).add_prefix("App Name_")
    expanded_df = pd.concat(
        [app_name_expanded, encoded_df.drop(columns=["App Name"], axis=1)],
        axis=1
    )

    # Trasformazione di encoded_user_input in un array di soli numeri
    expanded_user_input = []
    for value in encoded_user_input[0]:
        expanded_user_input.append(value)
    for value in encoded_user_input[1:]:
        expanded_user_input.append(value)

    # Normalizzazione e addestramento
    expanded_user_input = preprocessing.normalize([expanded_user_input])
    k_means = KMeans(n_clusters=4).fit(preprocessing.normalize(expanded_df))
    expanded_df["Cluster"] = k_means.labels_
    balanced_df["Cluster"] = expanded_df["Cluster"]

    # Predizione del cluster dell'utente
    prediction = k_means.predict(expanded_user_input)
    user_input_cluster = prediction[0]
    cluster_encoded_df = expanded_df[expanded_df["Cluster"] == user_input_cluster]
    cluster_encoded_df = cluster_encoded_df.drop(columns=["Cluster"], axis=1)
    cluster_balanced_df = balanced_df[balanced_df["Cluster"] == user_input_cluster].copy()

    # Calcolo similarità
    cluster_encoded_df["Similarity"] = cluster_encoded_df.apply(
        lambda row: cosine_similarity(expanded_user_input.reshape(1, -1), row.values.reshape(1, -1))[0][0], axis=1)
    cluster_balanced_df.loc[:, "Similarity"] = cluster_encoded_df["Similarity"]
    cluster_balanced_df = cluster_balanced_df.sort_values("Similarity", ascending=False)

    return cluster_balanced_df
