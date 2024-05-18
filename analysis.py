import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("dataset/clean-playstore-apps.csv")

# Distruzione dei Content Ratings
fig, ax = plt.subplots()
df['Content Rating'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
ax.set_title('Distribuzione dei Content Ratings')
ax.set_ylabel('')
plt.show()

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

# Distribuzione dei Downloads per Categoria
fig3, ax = plt.subplots()
df.groupby('Category')['Downloads'].sum().sort_values(ascending=False).plot(kind='barh', ax=ax, color='purple')
ax.set_title('Numero totale di Download per Categoria')
ax.set_xlabel('Numero di Download')
ax.set_ylabel('Categoria')
plt.show()

# Relazione tra Downloads e Editors Choice
fig4, ax = plt.subplots()
sns.scatterplot(data=df, x='Editors Choice', y='Downloads', ax=ax, linewidth=0)
ax.set_title('Relazione tra Downloads e Editors Choice')
ax.set_xlabel('Editors Choice')
ax.set_ylabel('Numero di Download')
ax.set_xticks([0, 1])
plt.show()

# Matrice di correlazione
df = df[["Rating", "Rating Count", "Downloads", "Price",
         "Content Rating", "Ad Supported", "In App Purchases", "Editors Choice"]]

df = pd.get_dummies(df, columns=["Content Rating"])
plt.figure(figsize=(15, 5))
sns.heatmap(df.corr(method="spearman"), annot=True)
plt.show()
