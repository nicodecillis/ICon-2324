import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('dataset/clean-playstore-apps.csv', na_filter=False)

print("Numero di campioni totali nel dataset prima del bilanciamento: ", len(df))

# BILANCIAMENTO RATINGS
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

# UNDERSAMPLING: rating 3.0 - 5.0
# le righe con download maggiori o uguali a 10 milioni devono essere escluse dall'undersampling
filtered_df = df[(df['Downloads'] >= 10000000) & (df['Rating'] >= min_undersampling/10) & (df['Rating'] <= max_undersampling/10)]
sample = pd.DataFrame()

for i in range(min_undersampling, max_undersampling+1):
    rating = i/10
    total_undersampling = pd.concat([total_undersampling, filtered_df[filtered_df['Rating'] == rating]])
    # per avere lo stesso numero di campioni per ogni rating, si sottrae il numero di campioni già presenti in total_undersampling
    sample = (df[(df['Rating'] == rating) & (df['Downloads'] < 10000000)]
              .sample(n=min_samples - len(total_undersampling[total_undersampling["Rating"] == rating]), random_state=42))
    total_undersampling = pd.concat([total_undersampling, sample])

df = df.drop(df[(df['Rating'] >= min_undersampling/10) & (df['Rating'] <= max_undersampling/10)
                & (~df['App Id'].isin(total_undersampling['App Id']))].index)
print("Numero di campioni totali dopo l'undersampling (rating 3.0 - 5.0): ", len(df))


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


# BILANCIAMENTO CATEGORIE
# UNDERSAMPLING
max_undersampling = df[df['Category'] == 'Reads']
categories = []
for cat in df['Category'].unique():
    if len(df[df['Category'] == cat]) > len(max_undersampling):
        categories.append(cat)
filtered_cat = pd.DataFrame()
for cat in categories:
    filtered_cat = pd.concat([filtered_cat, df[(df['Downloads'] >= 10000000) & (df['Category'] == cat)]])
    sample = (df[(df['Category'] == cat) & (df['Downloads'] < 10000000)]
                .sample(n=len(max_undersampling) - len(filtered_cat[filtered_cat['Category'] == cat]), random_state=42))
    filtered_cat = pd.concat([filtered_cat, sample])
    df = df.drop(df[(df['Category'] == cat) & (~df['App Id'].isin(filtered_cat['App Id']))].index)
print("Numero di campioni totali dopo l'undersampling delle categorie: ", len(df))


# OVERSAMPLING
min_oversampling = df[df['Category'] == 'Food & Drink']
categories = []
for cat in df['Category'].unique():
    if len(df[df['Category'] == cat]) < len(min_oversampling):
        categories.append(cat)
for cat in categories:
    sample = df[df['Category'] == cat].sample(n=len(min_oversampling) - len(df[df['Category'] == cat]), replace=True, random_state=42)
    df = pd.concat([df, sample])
print("Numero di campioni totali dopo l'oversampling delle categorie: ", len(df))

df.to_csv('dataset/balanced-playstore-apps.csv', index=False)

# Distribuzione dei Ratings
sns.barplot(x=df['Rating'].value_counts().index, y=df['Rating'].value_counts())
plt.xlabel('Rating')
plt.ylabel('Numero di App')
plt.title('Distribuzione dei Ratings')
plt.show()

# Distribuzione delle Categorie
fig2, ax = plt.subplots()
df['Category'].value_counts().plot(kind='barh', ax=ax)
ax.set_title('Distribuzione delle Categorie')
ax.set_xlabel('Numero di App')
plt.show()
