import sys
import os
from src.utils import print_table
from string import capwords
from pyswip import Prolog
from pyswip.prolog import PrologError
sys.path.append('.')


categories = ["Auto & Vehicles", "Beauty", "Communication", "Creativity", "Dating", "Education", "Entertainment",
              "Events", "Finance", "Food & Drink", "Games", "Health & Fitness", "House & Home", "Lifestyle",
              "Music & Audio", "Parenting", "Personalization", "Productivity", "Reads", "Shopping", "Tools",
              "Travel & Navigation", "Weather"]


def print_categories():
    print("Le categorie disponibili sono:")
    for c in categories:
        print("- ", c)


def use_kb():
    prolog = Prolog()

    current_dir = os.path.dirname(__file__)

    facts_path = os.path.join(current_dir, "facts.pl").replace("\\", "/")
    rules_path = os.path.join(current_dir, "rules.pl").replace("\\", "/")

    prolog.consult(facts_path)
    prolog.consult(rules_path)

    execute = True
    while execute:
        print("---- Esplorazione della Knowledge Base ----")
        print("1. Cerca app di uno specifico sviluppatore ordinate per download")
        print("2. Cerca app sotto un certo prezzo e con rating maggiore o uguale ad un certo valore")
        print("3. Cerca app poco scaricate ma con rating maggiore o uguale ad un certo valore")
        print("4. Cerca app di successo e con valutazione maggiore o uguale a un certo valore e ordinate per download")
        print("5. Cerca app sotto un certo prezzo e appartenenti ad una specifica categoria")
        print("6. Cerca app Editor's Choice appartenenti ad una specifica categoria e ordinate per download")
        print("7. Cerca app gratuite e con maggior numero di download")  # DA RIVEDERE
        print("8. Cerca app più costose ordinate per download\n")

        print("---- Statistiche della Knowledge Base ----")
        print("9. Ottieni il numero di app Editor's Choice appartenenti ad una specifica categoria")
        print("10. Ottieni la valutazione media per una specifica categoria")
        print("11. Ordina tutte le categorie per valutazione media")
        print("12. Ordina tutte le categorie per numero totale di download")  # DA RIVEDERE
        print("13. Cerca gli sviluppatori con più app di successo in una specifica categoria")
        print("X. Torna al menu principale\n")

        choice = input("Scegli un'opzione: ")
        try:
            if choice == "1":
                dev = input("Inserisci lo sviluppatore: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                try:
                    res = search_by_developer(prolog, dev, n)
                    clean_res = clean_data_two_col(res, 'TopAppsWithDownloads')
                    headers = ["Nome App", "Downloads"]
                    print_table(clean_res, headers)

                except IndexError:
                    count = query(prolog, f"count_apps_by_developer('{dev}', Count)")
                    if count[0]['Count'] == 0:
                        print(f"Nessuna app trovata per lo sviluppatore {dev}.\n")
                    else:
                        print("Il numero che hai inserito è troppo grande; riprova con un valore compreso tra 0 e "
                              + str(count[0]['Count']) + ".\n")

            elif choice == "2":
                price = input("Inserisci il prezzo massimo: ")
                rating = input("Inserisci il rating minimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_rating_price(prolog, rating, price, n)
                clean_res = clean_data_three_col(res, 'TopApps')
                headers = ["Nome App", "Valutazione", "Prezzo ($)"]
                print_table(clean_res, headers)

            elif choice == "3":
                rating = input("Inserisci il rating minimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_rating_low_downloads(prolog, rating, n)
                clean_res = clean_data_three_col(res, 'TopApps')
                headers = ["Nome App", "Valutazione", "Downloads"]
                print_table(clean_res, headers)

            elif choice == "4":
                rating = input("Inserisci il rating minimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_success_rating(prolog, rating, n)
                clean_res = clean_data_three_col(res, 'TopApps')
                headers = ["Nome App", "Downloads", "Valutazione"]
                print_table(clean_res, headers)

            elif choice == "5":
                print_categories()
                category = capwords(input("Inserisci la categoria: "))
                price = input("Inserisci il prezzo massimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                try:
                    res = search_by_category_price(prolog, category, price, n)
                    clean_res = clean_data_two_col(res, 'TopApps')
                    headers = ["Nome App", "Prezzo ($)"]
                    print_table(clean_res, headers)
                except IndexError:
                    if category not in categories:
                        print("La categoria inserita non esiste.\n")
                    else:
                        print("Inserisci un valore valido.\n")

            elif choice == "6":
                print_categories()
                category = capwords(input("Inserisci la categoria: "))
                n = input("Inserisci il numero di app da visualizzare: ")
                try:
                    res = search_by_category_edchoice(prolog, category, n)
                    clean_res = clean_data_two_col(res, 'TopApps')
                    headers = ["Nome App", "Downloads"]
                    print_table(clean_res, headers)
                except IndexError:
                    if category not in categories:
                        print("La categoria inserita non esiste.\n")
                    else:
                        num_apps = get_edchoice_by_category(prolog, category)[0]['EdChoiceApps']
                        print("Inserisci un numero di app compreso tra 0 e " + str(num_apps) + ".\n")

            elif choice == "7":
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_free_downloads(prolog, n)
                clean_res = clean_data_two_col(res, 'TopApps')
                headers = ["Nome App", "Downloads"]
                print_table(clean_res, headers)

            elif choice == "8":
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_expensive_downloads(prolog, n)
                clean_res = clean_data_three_col(res, 'TopApps')
                headers = ["Nome App", "Downloads", "Prezzo ($)"]
                print_table(clean_res, headers)

            elif choice == "9":
                print_categories()
                category = capwords(input("Inserisci la categoria: "))
                if category not in categories:
                    print("La categoria inserita non esiste.\n")
                else:
                    res = get_edchoice_by_category(prolog, category)
                    if res[0]['EdChoiceApps'] == 0:
                        print(f"Nessuna app Editor's Choice trovata nella categoria {category}.\n")
                    else:
                        print("Numero di app Editor's Choice nella categoria", category, ":",
                              res[0]['EdChoiceApps'], "\n")

            elif choice == "10":
                print_categories()
                category = capwords(input("Inserisci la categoria: "))
                try:
                    res = get_avg_rating_by_category(prolog, category)
                    print(f"Valutazione media nella categoria {category}: {res[0]['AvgRating']}", "\n")
                except PrologError:
                    print("La categoria inserita non esiste.\n")

            elif choice == "11":
                res = get_categories_ranked_by_rating(prolog)
                clean_res = clean_data_two_col(res, 'Categories')
                headers = ["Categoria", "Valutazione media"]
                print_table(clean_res, headers)

            elif choice == "12":
                res = get_categories_ranked_by_downloads(prolog)
                clean_res = clean_data_two_col(res, 'TotalDownloadsList')
                headers = ["Categoria", "Downloads totali"]
                print_table(clean_res, headers)

            elif choice == "13":
                print_categories()
                category = capwords(input("Inserisci la categoria: "))
                n = input("Inserisci il numero di sviluppatori da visualizzare: ")
                try:
                    res = get_devs_with_most_successful_apps(prolog, category, n)
                    clean_res = clean_data_two_col(res, 'Devs')
                    headers = ["Sviluppatore", "Numero app di successo"]
                    print_table(clean_res, headers)
                except IndexError:
                    if category not in categories:
                        print("La categoria inserita non esiste.\n")
                    elif int(n) < 0:
                        print("Inserisci un numero di sviluppatori maggiore di 0.\n")
                    else:
                        print("Inserisci un numero di sviluppatori inferiore.\n")

            elif choice.upper() == "X":
                execute = False

            else:
                print("Scelta non valida\n")

        except (IndexError, ValueError):
            print("Inserisci un valore valido.\n")

        except Exception as e:
            print(e)


def query(prolog, string):
    qr = (string + ".")
    return list(prolog.query(qr))


def search_by_developer(prolog, dev, n):
    n = int(n)
    dev = repr(dev)
    return query(prolog, f"top_downloads_by_developer({dev}, {n}, TopAppsWithDownloads)")


def search_by_rating_price(prolog, rating, price, n):
    n = int(n)
    rating = float(rating)
    price = float(price)
    return query(prolog, f"top_rating_price({rating}, {price}, {n}, TopApps)")


def search_by_rating_low_downloads(prolog, rating, n):
    n = int(n)
    rating = float(rating)
    return query(prolog, f"top_rating_low_downloads({rating}, {n}, TopApps)")


def search_by_success_rating(prolog, rating, n):
    n = int(n)
    rating = float(rating)
    return query(prolog, f"top_apps_by_rating({rating}, {n}, TopApps)")


def search_by_category_price(prolog, category, price, n):
    n = int(n)
    category = repr(category)
    return query(prolog, f"apps_by_category_price({category}, {price}, {n}, TopApps)")


def search_by_category_edchoice(prolog, category, n):
    n = int(n)
    category = repr(category)
    return query(prolog, f"top_editors_choice({category}, {n}, TopApps)")


def search_free_downloads(prolog, n):
    n = int(n)
    return query(prolog, f"top_free_downloads({n}, TopApps)")


def search_expensive_downloads(prolog, n):
    n = int(n)
    return query(prolog, f"top_expensive_downloads({n}, TopApps)")


def get_edchoice_by_category(prolog, category):
    category = repr(category)
    return query(prolog, f"count_editors_choice({category}, EdChoiceApps)")


def get_avg_rating_by_category(prolog, category):
    category = repr(category)
    return query(prolog, f"avg_rating_by_category({category}, AvgRating)")


def get_categories_ranked_by_rating(prolog):
    return query(prolog, f"categories_ranked_by_rating(Categories)")


def get_categories_ranked_by_downloads(prolog):
    return query(prolog, f"categories_ranked_by_downloads(TotalDownloadsList)")


def get_devs_with_most_successful_apps(prolog, category, n):
    n = int(n)
    category = repr(category)
    return query(prolog, f"top_developers_by_success({category}, {n}, Devs)")


def clean_data_two_col(res, key):
    res_data = res[0][key]
    cleaned_data = []
    for row in res_data:
        row = row.strip(",()")
        if ", b'" in row:
            name, value = row.split(", b'")
            value = value.strip("'")
        else:
            name, value = row.rsplit(", ", 1)
        cleaned_data.append((name, value))
    return cleaned_data


def clean_data_three_col(res, key):
    res_data = res[0][key]
    cleaned_data = []
    for row in res_data:
        row = row.strip(",()")
        name, value_couple = row.rsplit(", ,(", 1)
        value1, value2 = value_couple.rstrip(")").split(", ")
        if "b'" in value_couple:
            value1 = value1.strip("b'")
        cleaned_data.append((name, value1, value2))
    return cleaned_data
