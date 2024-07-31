import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec

"""
nltk.download('punkt')
nltk.download('stopwords')
"""


def preprocess(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    # Rimozione delle stopwords
    words = [word for word in words if word.isalpha() and word not in stop_words]
    return words


def get_embedding(tokens, model):
    vectors = [model.wv[word] for word in tokens if word in model.wv]
    if not vectors:
        return np.zeros(100)  # vettore nullo se non ci sono parole nel modello
    return np.mean(vectors, axis=0)


def encode_dataset(df):
    df = df.copy()
    df["App Name"] = df["App Name"].apply(preprocess)
    app_name_model = Word2Vec(sentences=df["App Name"], vector_size=100, window=5, min_count=1, workers=4)
    df["App Name"] = df["App Name"].apply(lambda tokens: get_embedding(tokens, app_name_model))

    for column in df.columns:
        if column not in ["App Name", "Content Rating"]:
            if df[column].dtype == type(object):
                df[column] = df[column].factorize()[0]

    df["Content Rating"] = df["Content Rating"].apply(lambda x: 3 if x == "Everyone" else 13 if x == "Teen" else 18)
    return df, app_name_model


def encode_user_input(user_input, app_name_model):
    user_input[4] = 3 if user_input[4] == "Everyone" else 13 if user_input[4] == "Teen" else 18
    user_input[0] = get_embedding(preprocess(user_input[0]), app_name_model)
    return user_input
