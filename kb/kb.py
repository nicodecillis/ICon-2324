from pyswip import Prolog
import pandas as pd


def write_facts(df):
    with open('facts.pl', 'w', encoding='utf-8') as f:
        for index, row in df.iterrows():
            app_id = row['App Id']
            app_name = row['App Name']
            price = row['Price']
            rating = row['Rating']
            downloads = row['Downloads']
            developer_id = row['Developer Id']
            category = row['Category']
            editors_choice = row['Editors Choice']
            success_rate = row['Success Rate']
            in_app_purchases = row['In App Purchases']
            ad_supported = row['Ad Supported']
            facts = [f"app_name({app_id}, {app_name})",
                     f"app_developer({app_name}, {developer_id})",
                     f"app_price_rating({app_name}, {price}, {rating})",
                     f"app_developer_downloads({app_name}, {developer_id}, {downloads})",
                     f"app_rating_downloads({app_name}, {rating}, {downloads})",
                     f"app_category_price({app_name}, {category}, {price})",
                     f"app_category_edchoice({app_name}, {category}, {editors_choice})",
                     f"app_category_downloads({app_name}, {category}, {downloads})",
                     f"app_category_rating({app_name}, {category}, {rating})",
                     f"app_price_downloads({app_name}, {price}, {downloads})",
                     f"app_category_developer_success({app_name}, {category}, {developer_id}, {success_rate})",
                     f"app_developer_success({app_name}, {developer_id}, {success_rate})",
                     f"app_success_purchases_downloads({app_name}, {success_rate}, {in_app_purchases}, {downloads})",
                     f"app_success_ad_downloads({app_name}, {success_rate}, {ad_supported}, {downloads})"]
            f.writelines("\n".join(facts) + "\n")
        f.close()


dataset = pd.read_csv('../dataset/balanced-playstore-apps.csv')
dataset = dataset.drop_duplicates()
write_facts(dataset)
