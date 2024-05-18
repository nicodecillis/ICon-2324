import pandas as pd



def normalization(min, max, value):
    return (value - min) / (max - min)


def success_rate(rating, downloads):
    return (rating + downloads) / 2


df = pd.read_csv('dataset/balanced-playstore-apps.csv')

df['Success Rate'] = None

min_download = df['Downloads'].min()
max_download = df['Downloads'].max()

min_rating = df['Rating'].min()
max_rating = df['Rating'].max()

for index, row in df.iterrows():
    normalized_rating = normalization(min_rating, max_rating, row['Rating'])
    normalized_downloads = normalization(min_download, max_download, row['Downloads'])
    success = success_rate(normalized_rating, normalized_downloads)
    df.at[index, 'Success Rate'] = round(success, 3)

df.to_csv('dataset/finalized-playstore-apps.csv', index=False)
