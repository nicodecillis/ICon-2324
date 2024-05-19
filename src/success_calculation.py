import pandas as pd

def normalization(min, max, value):
    return (value - min) / (max - min)


def success_rate(rating, downloads):
    return (rating + downloads) / 2

def calculate_success(df):
    min_download = df['Downloads'].min()
    max_download = 74000000

    min_rating = 0
    max_rating = 4.6

    for index, row in df.iterrows():
        downloads = min(row['Downloads'], max_download)
        rating = min(row['Rating'], max_rating)

        normalized_downloads = normalization(min_download, max_download, downloads)
        normalized_rating = normalization(min_rating, max_rating, rating)
        success = success_rate(normalized_rating, normalized_downloads)
        df.at[index, 'Success Rate'] = round(success, 1)*10
