import joblib


def predict(app_name, app_id, category, price, size, min_version, developer, content_rating, ad_supported,
            in_app_purchases, last_updated, balanced_df, encoded_df):

    dict = map_categorical_to_numeric(balanced_df, encoded_df)

    if app_name in dict["App Name"]:
        encoded_app_name = dict["App Name"][app_name]
    else:
        encoded_app_name = max(dict["App Name"].values()) + 1

    if app_id in dict["App Id"]:
        encoded_app_id = dict["App Id"][app_id]
    else:
        encoded_app_id = max(dict["App Id"].values()) + 1

    if category in dict["Category"]:
        encoded_category = dict["Category"][category]
    else:
        encoded_category = max(dict["Category"].values()) + 1

    if min_version in dict["Minimum Android"]:
        encoded_min_version = dict["Minimum Android"][min_version]
    else:
        encoded_min_version = max(dict["Minimum Android"].values()) + 1

    if developer in dict["Developer Id"]:
        encoded_developer = dict["Developer Id"][developer]
    else:
        encoded_developer = max(dict["Developer Id"].values()) + 1

    if content_rating in dict["Content Rating"]:
        encoded_content_rating = dict["Content Rating"][content_rating]
    else:
        encoded_content_rating = max(dict["Content Rating"].values()) + 1

    if last_updated in dict["Last Updated"]:
        encoded_last_updated = dict["Last Updated"][last_updated]
    else:
        encoded_last_updated = max(dict["Last Updated"].values()) + 1

    model = joblib.load("../learning/supervised/results/best_model.joblib")
    prediction = model.predict([[encoded_app_name, encoded_app_id, encoded_category, price, size, encoded_min_version,
                                 encoded_developer, encoded_content_rating, ad_supported, in_app_purchases,
                                 encoded_last_updated]])
    return prediction[0]


def map_categorical_to_numeric(balanced_df, encoded_df):
    mappings = {}
    columns = ["App Name", "App Id", "Category", "Minimum Android", "Developer Id", "Content Rating", "Last Updated"]

    for col in columns:
        unique_values = balanced_df[col].unique()
        unique_encoded_values = encoded_df[col].unique()
        mapping = dict(zip(unique_values, unique_encoded_values))
        mappings[col] = mapping

    return mappings
