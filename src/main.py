from utils import print_categories, print_content_ratings, calculate_norm_success, convert_success_rate

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
            category = ''
            price = 0
            app_name = ''
            content_rating = 0
            editors_choice = False
            downloads = 0
            rating = 0
            success_rate = 0

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
                if "gratuita" or "gratis" in price_str:
                    price = 0
                    break
                elif "pagamento" in price_str:
                    price = 1
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
                if "si" in chosen_editors_choice:
                    editors_choice = True
                    break
                elif "no" in chosen_editors_choice:
                    editors_choice = False
                    break
                else:
                    print("Input non valido. Riprova.")

            while True:
                chosen_downloads = input("Inserisci il numero minimo di download dell'app:\n")
                try:
                    downloads = int(chosen_downloads)
                    break
                except ValueError:
                    print("Numero di download non valido. Riprova.")

            while True:
                chosen_rating = input("Qual è il numero minimo di stelle (tra 1 e 5) che l'app deve possedere?\n")
                try:
                    rating = round(float(chosen_rating), 1)
                    if rating > 0 and rating <= 5:
                        break
                    else:
                        print("Input non valido: inserisci un numero compreso tra 1 e 5.")
                except ValueError or AttributeError:
                    print("Numero di stelle inserito non valido. Riprova.")

            # calcola success_rate
            print("downloads ", downloads, " - rating ", rating)
            success_rate = calculate_norm_success(downloads, rating)
            print("Success rate: ", success_rate)
            success_rate = convert_success_rate(success_rate)
            print("Success rate: ", success_rate)


        elif user_input == "2":
            pass
        elif user_input == "3":
            pass

main()
