import pandas as pd
import emoji
from google_play_scraper import app
import google_play_scraper.exceptions


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
                print(row["App Name"], " -- Rating: ", df.at[index, "Rating"], " -- Rating Count: ", df.at[index, "Rating Count"])
            except google_play_scraper.exceptions.NotFoundError:
                print(row["App Name"], "Not Found")
                df.drop(index, inplace=True)


def clean(dataset):
    df = pd.read_csv(dataset)

    df.drop(["Installs", "Minimum Installs", "Free", "Developer Email", "Developer Website", "Privacy Policy", "Scraped Time"], axis=1, inplace=True)

    df.rename(columns={"Maximum Installs": "Downloads"}, inplace=True)

    df.drop(df[df["Downloads"] < 100].index, inplace=True)
    df.drop(df[df["Rating Count"] < 15].index, inplace=True)

    #controlla contains_foreign_characters per ogni riga di "App Name" e se restituisce True, elimina la riga
    df.drop(df[df["App Name"].apply(contains_foreign_characters)].index, inplace=True)

    scrape_rating_info(df)

    df.to_csv("clean-playstore-apps.csv", index=False)


clean("playstore-apps.csv")

