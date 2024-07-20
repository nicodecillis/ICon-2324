import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def pie_plot(df, column, title):
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title(title)
    ax.set_ylabel('')
    plt.show()


def sns_bar_plot(df, column, title):
    sns.barplot(x=df[column].value_counts().index, y=df[column].value_counts())
    plt.xlabel(column)
    plt.ylabel('Numero di App')
    plt.title(title)
    plt.show()


def category_frequency_plot(df, title):
    fig, ax = plt.subplots()
    df['Category'].value_counts().plot(kind='barh', ax=ax)
    ax.set_title(title)
    ax.set_ylabel('Categoria')
    ax.set_xlabel('Numero di App')
    plt.show()


def category_downloads_plot(df, title):
    fig, ax = plt.subplots()
    df.groupby('Category')['Downloads'].sum().sort_values(ascending=False).plot(kind='barh', ax=ax, color='purple')
    ax.set_title(title)
    ax.set_xlabel('Numero di Downloads')
    ax.set_ylabel('Categoria')
    plt.show()


def scatter_plot(df, x, y, title):
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x, y=y, ax=ax, linewidth=0)
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel("Numero di " + y)
    ax.set_xticks([0, 1])
    plt.show()


def correlation_matrix(df, title):
    df = df[["Rating", "Rating Count", "Downloads", "Price ($)", "Ad Supported",
             "In App Purchases", "Editors Choice", "Success Rate"]]
    df = pd.get_dummies(df, columns=["Success Rate"])
    plt.figure(figsize=(15, 5))
    sns.heatmap(df.corr(method="spearman"), annot=True)
    plt.title(title)
    plt.show()


try:
    df_preprocessed = pd.read_csv("../dataset/preprocessed-playstore-apps.csv")
    df_balanced = pd.read_csv("../dataset/balanced-playstore-apps.csv")

    # Distribuzione dei Content Ratings
    pie_plot(df_preprocessed, 'Content Rating', "Distribuzione dei Content Ratings nel dataset pre-processato")
    pie_plot(df_balanced, 'Content Rating', "Distribuzione dei Content Ratings nel dataset bilanciato")

    # Distribuzione dei Ratings
    sns_bar_plot(df_preprocessed, 'Rating', "Distribuzione dei Ratings nel dataset pre-processato")
    sns_bar_plot(df_balanced, 'Rating', "Distribuzione dei Ratings nel dataset bilanciato")

    # Distribuzione delle Categorie
    category_frequency_plot(df_preprocessed, "Distribuzione delle Categorie nel dataset pre-processato")
    category_frequency_plot(df_balanced, "Distribuzione delle Categorie nel dataset bilanciato")

    # Distribuzione dei Downloads per Categoria
    category_downloads_plot(df_preprocessed, "Numero totale di Download per Categoria nel dataset pre-processato")
    category_downloads_plot(df_balanced, "Numero totale di Download per Categoria nel dataset bilanciato")

    # Distribuzione dei Success Rate
    sns_bar_plot(df_preprocessed, 'Success Rate', 'Distribuzione dei Success Rate nel dataset pre-processato')
    pie_plot(df_balanced, 'Success Rate', 'Distribuzione dei Success Rate nel dataset bilanciato')

    # Relazione tra Downloads e Editors Choice
    scatter_plot(df_preprocessed, 'Editors Choice', 'Downloads', 'Relazione tra Downloads e Editors Choice nel dataset pre-processato')
    scatter_plot(df_balanced, 'Editors Choice', 'Downloads', 'Relazione tra Downloads e Editors Choice nel dataset bilanciato')

    # Matrice di correlazione
    correlation_matrix(df_preprocessed, "Matrice di Correlazione nel dataset pre-processato")
    correlation_matrix(df_balanced, "Matrice di Correlazione nel dataset bilanciato")

except KeyboardInterrupt:
    pass
