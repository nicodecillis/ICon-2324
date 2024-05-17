import pandas as pd

df = pd.read_csv('dataset/clean-playstore-apps.csv')

total_undersampling = pd.DataFrame()
min_undersampling = 30
max_undersampling = 50

min_oversampling = 10
max_oversampling = 29

# Ricerca minimo numero di campioni per rating
min_samples = len(df)
for i in range(min_undersampling, max_undersampling+1):
    rating = i/10
    if len(df[df['Rating'] == rating]) < min_samples:
        min_samples = len(df[df['Rating'] == rating])
print("Numero campioni per rating: ", min_samples)


# UNDERSAMPLING: rating 3.0 - 5.0
# le righe con download maggiori di 10milioni devono essere escluse dall'undersampling
filtered_df = df[(df['Downloads'] > 10000000) & (df['Rating'] >= min_undersampling/10) & (df['Rating'] <= max_undersampling/10)]
sample = pd.DataFrame()

for i in range(min_undersampling, max_undersampling+1):
    rating = i/10
    total_undersampling = pd.concat([total_undersampling, filtered_df[filtered_df['Rating'] == rating]])
    # per avere lo stesso numero di campioni per ogni rating, si sottrae il numero di campioni già presenti in total_undersampling
    sample = (df[(df['Rating'] == rating) & (df['Downloads'] < 10000000)]
              .sample(n=min_samples - len(total_undersampling[total_undersampling["Rating"] == rating]), random_state=42))
    total_undersampling = pd.concat([total_undersampling, sample])

df = df.drop(df[(df['Rating'] >= min_undersampling/10) & (df['Rating'] <= max_undersampling/10) & (~df['App Id'].isin(total_undersampling['App Id']))].index)
print("Numero di campioni totali dopo l'undersampling: ", len(df))


# OVERSAMPLING: rating 1.0 - 2.9
total_oversampling = pd.DataFrame()
for i in range(min_oversampling, max_oversampling+1):
    rating = i/10
    # per avere lo stesso numero di campioni per ogni rating, si sottrae il numero di campioni già presenti in df con quel rating
    sample = df[df['Rating'] == rating].sample(n=min_samples - len(df[df['Rating'] == rating]), replace=True, random_state=42)
    total_oversampling = pd.concat([total_oversampling, sample])
df = pd.concat([df, total_oversampling])
print("Numero di campioni totali dopo l'oversampling (rating 1.0 - 2.9): ", len(df))


# OVERSAMPLING: rating 0
sample = df[df['Rating'] == 0].sample(n=min_samples-len(df[df['Rating'] == 0]), replace=True, random_state=42)
df = pd.concat([df, sample])
print("Numero di campioni totali dopo l'oversampling (rating 0): ", len(df))


#stampa barplot rating
import seaborn as sns
import matplotlib.pyplot as plt
sns.barplot(x=df['Rating'].value_counts().index, y=df['Rating'].value_counts())
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Distribution of Ratings')
plt.show()


df.to_csv('dataset/balanced-playstore-apps.csv', index=False)
