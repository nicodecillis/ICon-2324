import pandas as pd
import emoji
from google_play_scraper import app
import google_play_scraper.exceptions
import sys
sys.path.append('.')
from src.utils import add_success_rate_in_rows


def group_categories(df):
    df['Category'] = df['Category'].replace(['Action', 'Adventure', 'Arcade', 'Casino', 'Card', 'Casual', 'Educational',
                                             'Music', 'Puzzle', 'Racing', 'Role Playing', 'Simulation', 'Strategy',
                                             'Trivia', 'Word', 'Board'], 'Games')
    df['Category'] = df['Category'].replace(['Art & Design', 'Photography'], 'Creativity')
    df['Category'] = df['Category'].replace(['Books & Reference', 'Comics', 'News & Magazines'], 'Reads')
    df['Category'] = df['Category'].replace(['Business', 'Finance'], 'Finance')
    df['Category'] = df['Category'].replace(['Communication', 'Social'], 'Communication')
    df['Category'] = df['Category'].replace(['Health & Fitness', 'Medical', 'Sports'], 'Health & Fitness')
    df['Category'] = df['Category'].replace(['Maps & Navigation', 'Travel & Local'], 'Travel & Navigation')
    df['Category'] = df['Category'].replace(['Tools', 'Libraries & Demo'], 'Tools')
    df['Category'] = df['Category'].replace(['Productivity', 'Video Players & Editors'], 'Productivity')


def group_content_rating(df):
    df['Content Rating'] = df['Content Rating'].replace(['Everyone', 'Unrated'], 'Everyone')
    df['Content Rating'] = df['Content Rating'].replace(['Everyone 10+', 'Teen'], 'Teen')
    df['Content Rating'] = df['Content Rating'].replace(['Mature 17+', 'Adults only 18+'], 'Adults')


def contains_foreign_characters(text):
    text = str(text)
    max_ascii_range = 255
    blank_emoji = 65039

    for i in range(0, len(text)):
        if not emoji.is_emoji(text[i]):
            if ord(text[i]) > max_ascii_range:
                if ord(text[i]) != blank_emoji:
                    return True
    return False


def scrape_rating_info(df):
    for index, row in df.iterrows():
        if pd.isnull(row["Rating"]):
            try:
                result = app(row["App Id"])
                if result["score"] is None:
                    df.at[index, "Rating"] = 0
                    df.at[index, "Rating Count"] = 0
                else:
                    df.at[index, "Rating"] = round(result["score"], 1)
                    df.at[index, "Rating Count"] = result["ratings"]
            except google_play_scraper.exceptions.NotFoundError:
                print(row["App Name"], "Not Found")
                df.drop(index, inplace=True)


def scrape_unrated_apps(df):
    for index, row in df.iterrows():
        if row["Content Rating"] == "Unrated":
            try:
                result = app(row["App Id"])
                df.at[index, "Content Rating"] = result["contentRating"]
            except google_play_scraper.exceptions.NotFoundError:
                print(row["App Name"], "Not Found")
                df.drop(index, inplace=True)


def convert_size(df):
    df["Size (MB)"] = df["Size (MB)"].str.replace(',', '')
    df.loc[df["Size (MB)"].str.endswith('k'), "Size (MB)"] = df.loc[df["Size (MB)"].str.endswith('k'), "Size (MB)"].apply(
        lambda x: str(float(x[:-1]) / 1024) + 'M')
    df.loc[df["Size (MB)"].str.endswith('G'), "Size (MB)"] = df.loc[df["Size (MB)"].str.endswith('G'), "Size (MB)"].apply(
        lambda x: str(float(x[:-1]) * 1024) + 'M')
    df.loc[df["Size (MB)"].str.endswith('M'), "Size (MB)"] = df.loc[df["Size (MB)"].str.endswith('M'), "Size (MB)"].apply(lambda x: x[:-1])
    df["Size (MB)"] = df["Size (MB)"].apply(lambda x: round(float(x), 2) if x != "Varies with device" else x)


def clean(df):
    df.drop(["Installs", "Minimum Installs", "Free", "Developer Email",
             "Developer Website", "Released", "Privacy Policy", "Scraped Time"], axis=1, inplace=True)

    df.rename(columns={"Maximum Installs": "Downloads"}, inplace=True)
    df.rename(columns={"Price": "Price ($)"}, inplace=True)
    df.rename(columns={"Size (MB)": "Size (MB)"}, inplace=True)

    df.drop(df[df["Downloads"] < 1000].index, inplace=True)
    df.drop(df[df["Rating Count"] < 50].index, inplace=True)
    df.drop("Currency", axis=1, inplace=True)

    # controlla contains_foreign_characters per ogni riga di "App Name" e se restituisce True, elimina la riga
    df.drop(df[df["App Name"].apply(contains_foreign_characters)].index, inplace=True)

    df["Rating Count"] = df["Rating Count"].astype(int)

    # aggiunta dei nomi delle app mancanti
    df.loc[pd.isnull(df["App Name"]), "App Name"] = df.loc[pd.isnull(df["App Name"]), "App Id"].apply(lambda x: app(x)["title"])

    scrape_rating_info(df)
    # controllo inconsistenze tra Rating Count e Downloads
    df.drop(df[df["Rating Count"] > df["Downloads"]].index, inplace=True)

    df.loc[pd.isnull(df["Minimum Android"]), "Minimum Android"] = "Varies with device"

    # aggiunta manuale delle dimensioni mancanti
    df.loc[df["App Id"] == "com.cuberobotics.susu", "Size (MB)"] = "16.4M"
    df.loc[df["App Id"] == "com.zkteco.intelitime", "Size (MB)"] = "2.9M"
    df.loc[df["App Id"] == "com.dormstudios.away", "Size (MB)"] = "Varies with device"

    scrape_unrated_apps(df)
    # aggiunta manuale dei Content Rating non specificati
    df.loc[df["App Id"] == "com.Shumbolag", "Content Rating"] = "Everyone"
    df.loc[df["App Id"] == "cz.inzeratyzdarma.cz", "Content Rating"] = "Mature 17+"
    df.loc[df["App Id"] == "clumsy.cheatingdevz.com.clumsybirdcheat", "Content Rating"] = "Everyone"
    df.loc[df["App Id"] == "com.jb.gosms.pctheme.moji", "Content Rating"] = "Everyone"
    # raggruppamento dei Content Rating
    group_content_rating(df)

    # raggruppamento delle Categorie
    group_categories(df)
    convert_size(df)


def add_success_rate_col(df):
    df['Success Rate'] = None
    add_success_rate_in_rows(df)


dataset = pd.read_csv("../dataset/playstore-apps.csv")
clean(dataset)
add_success_rate_col(dataset)
dataset.to_csv("dataset/preprocessed-playstore-apps.csv", index=False)
