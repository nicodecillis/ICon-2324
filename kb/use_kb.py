from pyswip import Prolog
from pyswip.prolog import PrologError


def use_KB ():
    prolog = Prolog()
    prolog.consult("facts.pl")
    prolog.consult("rules.pl")

    print("Benvenuto!")
    execute = True
    while (execute):
        print("---- Esplorazione della Knowledge Base ----")
        print("1. Cerca app di uno specifico sviluppatore ordinate per download")   # DA RIVEDERE (es. Google LLC)
        print("2. Cerca app sotto un certo prezzo e con rating maggiore o uguale ad un certo valore")
        print("3. Cerca app poco scaricate ma con rating maggiore o uguale ad un certo valore")
        print("4. Cerca app di successo e con valutazione maggiore o uguale a un certo valore e ordinate per download")
        print("5. Cerca app sotto un certo prezzo e appartenenti ad una specifica categoria")
        print("6. Cerca app Editor's Choice appartenenti ad una specifica categoria e ordinate per download")
        print("7. Cerca app gratuite e con maggior numero di download")     # DA RIVEDERE
        print("8. Cerca app più costose ma con maggior numero di download\n")

        print("---- Statistiche della Knowledge Base ----")
        print("9. Ottieni il numero di app Editor's Choice appartenenti ad una specifica categoria")
        print("10. Ottieni la valutazione media per una specifica categoria")
        print("11. Ordina tutte le categorie per valutazione media")
        print("12. Ordina tutte le categorie per numero totale di download")    # DA RIVEDERE
        print("13. Cerca gli sviluppatori con più app di successo in una specifica categoria")
        print("X. Uscita\n")

        choice = input("Scegli un'opzione: ")
        try:
            if choice == "1":
                dev = input("Inserisci lo sviluppatore: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_developer(prolog, dev, n)
                for r in res[0]['TopAppsWithDownloads']:
                    print(r)

            elif choice == "2":
                price = input("Inserisci il prezzo massimo: ")
                rating = input("Inserisci il rating minimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_rating_price(prolog, rating, price, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "3":
                rating = input("Inserisci il rating minimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_rating_low_downloads(prolog, rating, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "4":
                rating = input("Inserisci il rating minimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_success_rating(prolog, rating, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "5":
                print_categories()
                category = input("Inserisci la categoria: ")
                price = input("Inserisci il prezzo massimo: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_category_price(prolog, category, price, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "6":
                print_categories()
                category = input("Inserisci la categoria: ")
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_by_category_edchoice(prolog, category, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "7":
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_free_downloads(prolog, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "8":
                n = input("Inserisci il numero di app da visualizzare: ")
                res = search_expensive_downloads(prolog, n)
                for r in res[0]['TopApps']:
                    print(r)

            elif choice == "9":
                print_categories()
                category = input("Inserisci la categoria: ")
                res = get_edchoice_by_category(prolog, category)
                print("Numero di app Editor's Choice nella categoria", category, ":", res[0]['EdChoiceApps'])

            elif choice == "10":
                print_categories()
                category = input("Inserisci la categoria: ")
                res = get_avg_rating_by_category(prolog, category)
                print(f"Valutazione media nella categoria {category}: {res[0]['AvgRating']}")

            elif choice == "11":
                res = get_categories_ranked_by_rating(prolog)
                for r in res[0]['Categories']:
                    print(r)

            elif choice == "12":
                res = get_categories_ranked_by_downloads(prolog)
                print(res)

            elif choice == "13":
                print_categories()
                category = input("Inserisci la categoria: ")
                n = input("Inserisci il numero di sviluppatori da visualizzare: ")
                res = get_devs_with_most_successful_apps(prolog, category, n)
                for r in res[0]['Devs']:
                    print(r)

            elif choice.upper() == "X":
                print("Arrivederci!")
                execute = False

            else:
                print("Scelta non valida\n")

        except IndexError:
            print("Il numero che hai inserito è troppo grande; riprova con un valore inferiore.\n")

        # aggiungi eccezione per input non valido
        except ValueError:
            print("Inserisci un valore valido.\n")

        except PrologError as e:
            print("Inserisci una categoria valida.\n")
            print(e)

        except Exception as e:
            #print("Errore nell'esecuzione dell'operazione\n")
            print(e)
            print(type(e).__name__)


def query(prolog, str):
    qr = (str + ".")
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


def print_categories():
    print("Le categorie disponibili sono:")
    print("- Auto & Vehicles")
    print("- Beauty")
    print("- Communication")
    print("- Creativity")
    print("- Dating")
    print("- Education")
    print("- Entertainment")
    print("- Events")
    print("- Finance")
    print("- Food & Drink")
    print("- Games")
    print("- Health & Fitness")
    print("- House & Home")
    print("- Lifestyle")
    print("- Music & Audio")
    print("- Parenting")
    print("- Personalization")
    print("- Productivity")
    print("- Reads")
    print("- Shopping")
    print("- Tools")
    print("- Travel & Navigation")
    print("- Weather")


use_KB()