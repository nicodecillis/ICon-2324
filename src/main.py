import pandas as pd
from kb.use_kb import use_kb
from prediction import predict

from utils import print_categories, print_content_ratings, calculate_norm_success, convert_success_rate, print_table
from recommender import find_recommendations

categories = ["Auto & Vehicles", "Beauty", "Communication", "Creativity", "Dating", "Education", "Entertainment",
              "Events", "Finance", "Food & Drink", "Games", "Health & Fitness", "House & Home", "Lifestyle",
              "Music & Audio", "Parenting", "Personalization", "Productivity", "Reads", "Shopping", "Tools",
              "Travel & Navigation", "Weather"]
content_ratings = ["Everyone", "Teen", "Adults"]


def main(balanced_df, encoded_df):
    exit = False
    print("Benvenuto!\n")
    while not exit:
        print("Scegli una delle seguenti opzioni:\n"
              "1 - Raccomandazione di app simili\n"
              "2 - Predizione del tasso di successo di un app non ancora sul mercato\n"
              "3 - Esplorazione della base di conoscenza\n"
              "X - Esci")

        user_input = input()

        if user_input.upper() == "X":  # X per uscire
            print("Arrivederci!")
            break
        elif user_input == "1":
            print_categories(categories)
            while True:
                chosen_category = input("Quale categoria di app stai cercando?\n").title()
                if chosen_category in categories:
                    category = chosen_category
                    break
                else:
                    print("Categoria non valida. Riprova.")

            while True:
                price_str = input("Cerchi un'app gratuita o a pagamento?\n").lower()
                if "gratuita" in price_str or "gratis" in price_str:
                    price = 0
                    break
                elif "pagamento" in price_str:
                    while True:
                        try:
                            price_str = input("Quanto pagheresti per l'app?\n")
                            price = float(price_str)
                            break
                        except ValueError:
                            print("Prezzo non valido. Riprova.")
                    break
                else:
                    print("Input non valido. Riprova.")

            app_name = input("Suggeriscimi il nome di un'app di tuo gradimento appartenente a questa categoria:\n")

            while True:
                print_content_ratings(content_ratings)
                chosen_content_rating = input("Quale dovrebbe essere la classificazione dei contenuti dell'app?\n").title()
                if "Everyone" in chosen_content_rating:
                    content_rating = "Everyone"
                    break
                elif "Teen" in chosen_content_rating:
                    content_rating = "Teen"
                    break
                elif "Adults" in chosen_content_rating:
                    content_rating = "Teen"
                    break
                else:
                    print("Input non valido. Riprova.")

            while True:
                print("Un'app \"Editor's Choice\" è un'app scelta dalla redazione come una delle app più "
                      "innovative, creative e degne di nota presenti nello store.")
                chosen_editors_choice = input("Stai cercando un'app Editor's Choice?\n").lower()
                if "si" in chosen_editors_choice or "sì" in chosen_editors_choice:
                    editors_choice = True
                    break
                elif "no" in chosen_editors_choice:
                    editors_choice = False
                    break
                else:
                    print("Input non valido. Riprova.")

            while True:
                chosen_downloads = input("Inserisci il numero di download che l'app dovrebbe avere:\n")
                try:
                    downloads = int(chosen_downloads)
                    break
                except ValueError:
                    print("Numero di download non valido. Riprova.")

            while True:
                chosen_rating = input("Qual è il numero minimo di stelle (tra 1 e 5) che l'app deve possedere?\n")
                try:
                    rating = round(float(chosen_rating), 1)
                    if 0 < rating <= 5:
                        break
                    else:
                        print("Input non valido: inserisci un numero compreso tra 1 e 5.")
                except ValueError or AttributeError:
                    print("Numero di stelle inserito non valido. Riprova.")

            # calcola success_rate
            success_rate = calculate_norm_success(downloads, rating)
            success_rate = convert_success_rate(success_rate)

            print("Ricerca delle app simili...")
            recommended_apps = find_recommendations(app_name, category, rating, downloads, price, content_rating,
                                                    editors_choice, success_rate)

            print("Ecco le applicazioni suggerite in base alle tue richieste:")
            columns = ["App Name", "Rating", "Downloads", "Price ($)", "Editors Choice", "Success Rate"]
            recommended_apps = recommended_apps[columns]
            data_list = recommended_apps.values.tolist()
            print_table(data_list, columns, paginate=True)

        elif user_input == "2":
            while True:
                app_name = input("Come si chiama la tua app?\n").lower()
                if app_name == "":
                    print("Nome non valido. Riprova.")
                else:
                    break

            while True:
                app_id = input("Inserisci il package name dell'app:\n").lower()
                if app_id in balanced_df["App Id"].values:
                    print("Il package name inserito è stato già assegnato ad un'altra app. Riprova con uno univoco.")
                elif app_id == "":
                    print("Package name non valido. Riprova.")
                else:
                    break

            while True:
                developer = input("Qual è il tuo nome da sviluppatore?\n")
                if developer == "":
                    print("Nome non valido. Riprova.")
                else:
                    break

            while True:
                print_categories(categories)
                chosen_category = input("A quale categoria appartiene l'app?\n").title()
                if chosen_category in categories:
                    category = chosen_category
                    break
                else:
                    print("Categoria non valida. Riprova.")

            while True:
                price_str = input("Quanto costa l'app in $?\n")
                try:
                    price = float(price_str)
                    break
                except ValueError:
                    print("Prezzo non valido. Riprova.")

            while True:
                size_str = input("Quanto spazio occupa l'app in MB?\n")         # TODO: inserire Varies with Device
                try:
                    size = float(size_str)
                    break
                except ValueError:
                    print("Dimensione non valida. Riprova.")

            android_versions = ["1.0", "1.1", "1.5", "1.6", "2.0", "2.0.1", "2.1", "2.2", "2.2.1", "2.2.2", "2.2.3",
                                "2.3", "2.3 - 4.4", "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7",
                                "3.0", "3.1", "3.2", "3.2.1", "3.2.2", "3.2.3", "3.2.4", "3.2.5", "3.2.6", "4.0",
                                "4.0 - 6.0", "4.0.1", "4.0.2", "4.0.3", "4.0.3 - 8.0", "4.0.4", "4.1", "4.1.1", "4.1.2",
                                "4.2", "4.2 - 4.4W", "4.2.1", "4.2.2", "4.3", "4.3 - 4.4", "4.3.1", "4.4", "4.4.1",
                                "4.4.2", "4.4.3", "4.4.4", "4.4W", "5.0", "5.0 - 8.0", "5.0.1", "5.0.2", "5.1", "5.1.1",
                                "6.0", "6.0.1", "6.0 - 7.1.1", "7.0", "7.1", "7.1.1", "7.1.2", "8.0", "8.1", "9", "10",
                                "11", "12", "13", "14"]

            while True:
                version = input("Qual è la minima versione di Android supportata dall'app?\n"
                                "Se la versione dipende dal dispositivo, scrivi \"Varies with device\".\n").upper()
                if version.capitalize() == "Varies with device":
                    version = version.capitalize()
                    break
                if version in android_versions:
                    break
                else:
                    print("Versione di Android non valida. Riprova.")
            if "-" not in version and version.capitalize() != "Varies with device":
                version = version + " and up"

            while True:
                print_content_ratings(content_ratings)
                chosen_content_rating = input(
                    "Qual è la classificazione dei contenuti dell'app?\n").title()
                if "Everyone" in chosen_content_rating:
                    content_rating = "Everyone"
                    break
                elif "Teen" in chosen_content_rating:
                    content_rating = "Teen"
                    break
                elif "Adults" in chosen_content_rating:
                    content_rating = "Teen"
                    break
                else:
                    print("Input non valido. Riprova.")

            while True:
                chosen_ad_supported = input("L'applicazione include pubblicità?\n").lower()
                if "si" in chosen_ad_supported or "sì" in chosen_ad_supported:
                    ad_supported = True
                    break
                elif "no" in chosen_ad_supported:
                    ad_supported = False
                    break
                else:
                    print("Input non valido. Riprova.")

            while True:
                chosen_app_purchases = input("L'applicazione prevede acquisti in-app?\n").lower()
                if "si" in chosen_app_purchases or "sì" in chosen_app_purchases:
                    in_app_purchases = True
                    break
                elif "no" in chosen_app_purchases:
                    in_app_purchases = False
                    break
                else:
                    print("Input non valido. Riprova.")

            while True:
                last_updated = input("A quando risale l'ultimo aggiornamento dell'app?\n"
                                     "Inserisci la data nel formato seguente: es. \"Jan 01, 2024\".\n").capitalize()
                try:
                    last_updated = pd.to_datetime(last_updated, format="%b %d, %Y").strftime("%b %d, %Y")
                    break
                except ValueError:
                    print("Data non valida. Riprova.")

            prediction_value = predict(app_name, app_id, category, price, size, version, developer, content_rating,
                                       ad_supported, in_app_purchases, last_updated, balanced_df, encoded_df)
            success_rates = {1: "non molto popolare",
                             2: "mediamente popolare",
                             3: "popolare",
                             4: "molto popolare"}
            print("La tua app potrebbe diventare " + success_rates[prediction_value] + "!\n")

        elif user_input == "3":
            print("Caricamento della base di conoscenza...")
            use_kb()

        else:
            print("Input non valido. Riprova.")

balanced_df = pd.read_csv("../dataset/balanced-playstore-apps.csv")
encoded_df = pd.read_csv("../dataset/encoded-playstore-apps.csv")
main(balanced_df, encoded_df)
