from utils import print_categories, print_content_ratings, calculate_norm_success, convert_success_rate, print_table
from recommender import find_recommendations

categories = ["Auto & Vehicles", "Beauty", "Communication", "Creativity", "Dating", "Education", "Entertainment",
              "Events", "Finance", "Food & Drink", "Games", "Health & Fitness", "House & Home", "Lifestyle",
              "Music & Audio", "Parenting", "Personalization", "Productivity", "Reads", "Shopping", "Tools",
              "Travel & Navigation", "Weather"]
content_ratings = ["Everyone", "Teen", "Adults"]


def main():
    exit = False
    print("Benvenuto sulla CagataIntergalattica!\n")
    while not exit:
        print("Scegli una delle seguenti opzioni:\n"
              "1 - Raccomandazione di app simili\n"
              "2 - Predizione del tasso di successo di un app non ancora sul mercato\n"
              "3 - Esplorazione della base di conoscenza\n"
              "X - Esci\n")

        user_input = input()

        if user_input.upper() == "X":  # X per uscire
            print("Arrivederci!")
            break
        elif user_input == "1":
            print_categories(categories)
            while True:
                chosen_category = input("Quale categoria di app stai cercando?\n").capitalize()
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
                chosen_content_rating = input("Quale dovrebbe essere la classificazione dei contenuti dell'app?\n").capitalize()
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
            pass
        elif user_input == "3":
            pass


main()
