import pandas as pd


def write_facts(df):
    with open('facts.pl', 'w', encoding='utf-8') as f:
        facts_list = [
            ":- discontiguous app_name/2.",
            ":- discontiguous app_rating_price/3.",
            ":- discontiguous app_developer/2.",
            ":- discontiguous app_developer_downloads/3.",
            ":- discontiguous app_rating_downloads/3.",
            ":- discontiguous app_category/2.",
            ":- discontiguous app_category_price/3.",
            ":- discontiguous app_category_edchoice/3.",
            ":- discontiguous app_category_edchoice_downloads/4.",
            ":- discontiguous app_category_downloads/3.",
            ":- discontiguous app_category_rating/3.",
            ":- discontiguous app_price_downloads/3.",
            ":- discontiguous app_category_developer_success/4.",
            ":- discontiguous app_success_rating_downloads/4."
        ]

        f.writelines("\n".join(facts_list) + "\n")

        for index, row in df.iterrows():
            app_id = str(row['App Id'])
            app_name = str(row['App Name'])
            price = row['Price ($)']
            rating = row['Rating']
            downloads = row['Downloads']
            developer_id = str(row['Developer Id'])
            category = row['Category']
            editors_choice = row['Editors Choice']
            success_rate = row['Success Rate']

            # controlla se in developer_id o app_name ci sono " ed eliminali
            if "'" in app_name:
                app_name = app_name.replace("'", '')

            if "'" in developer_id:
                developer_id = developer_id.replace("'", '')

            app_id = f"'{app_id}'"
            app_name = f"'{app_name}'"
            developer_id = f"'{developer_id}'"
            category = f"'{category}'"
            editors_choice = f"'{editors_choice}'"
            success_rate = f"'{success_rate}'"

            facts = [f"app_name({app_id},{app_name}).",
                     f"app_rating_price({app_name},{rating},{price}).",
                     f"app_developer({app_name},{developer_id}).",
                     f"app_developer_downloads({app_name},{developer_id},{downloads}).",
                     f"app_rating_downloads({app_name},{rating},{downloads}).",
                     f"app_category({app_name},{category}).",
                     f"app_category_price({app_name},{category},{price}).",
                     f"app_category_edchoice({app_name},{category},{editors_choice}).",
                     f"app_category_edchoice_downloads({app_name},{category},{editors_choice},{downloads}).",
                     f"app_category_downloads({app_name},{category},{downloads}).",
                     f"app_category_rating({app_name},{category},{rating}).",
                     f"app_price_downloads({app_name},{price},{downloads}).",
                     f"app_category_developer_success({app_name},{category},{developer_id},{success_rate}).",
                     f"app_success_rating_downloads({app_name},{success_rate},{rating},{downloads})."]
            f.writelines("\n".join(facts) + "\n")
        f.close()


def write_rules(rules):
    with open('rules.pl', 'w', encoding='utf-8') as f:
        f.write(rules)
        f.close()


dataset = pd.read_csv('../dataset/balanced-playstore-apps.csv')
dataset = dataset.drop_duplicates()
write_facts(dataset)

rules = """% Predicato per restituire i primi N elementi di una lista
take(0, _, []).
take(N, [Head|Tail], [Head|Taken]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Tail, Taken).
    
% Predicato ausiliario per contare le occorrenze di un elemento in una lista
count_occurrences(_, [], 0).
count_occurrences(Elem, [Elem|Tail], Count) :-
    count_occurrences(Elem, Tail, SubCount),
    Count is SubCount + 1.
count_occurrences(Elem, [Head|Tail], Count) :-
    Elem \\= Head,
    count_occurrences(Elem, Tail, Count).

% Predicato che conta il numero totale di app per uno sviluppatore
count_apps_by_developer(Dev, Count) :-
    findall(AppName, app_developer(AppName, Dev), AppList),
    length(AppList, Count).

% Predicato per ottenere una lista di N app entro una certa soglia di prezzo e con una valutazione superiore o uguale a un certo valore
top_rating_price(RatingTh, PriceTh, N, TopApps) :- 
    findall((AppName, Rating, Price), (app_rating_price(AppName, Rating, Price), Price =< PriceTh, Rating >= RatingTh), AppList),
    sort(2, @>=, AppList, SortedApps),
    take(N, SortedApps, TopApps).

% Predicato per ottenere una lista di N app ordinate per numero di download per uno sviluppatore dato
top_downloads_by_developer(Dev, N, TopAppsWithDownloads) :-
    findall((AppName, Downloads), app_developer_downloads(AppName, Dev, Downloads), AppsWithDownloads),
    sort(2, @>=, AppsWithDownloads, SortedAppsWithDownloads),
    % trasforma Downloads in stringa con atom_string
    maplist([Tuple, NewTuple]>>(Tuple = (A,IntegerB), atom_string(IntegerB, StringB), NewTuple = (A,StringB)), SortedAppsWithDownloads, ConvertedList),
    take(N, ConvertedList, TopAppsWithDownloads).
    
% Predicato per ottenere una lista di N app con rating maggiore o uguale ad un certo valore ma poco scaricate
top_rating_low_downloads(RatingTh, N, TopApps) :-
    findall((AppName, Rating, Downloads), app_rating_downloads(AppName, Rating, Downloads), AppList),
    include([(_, Rating, Downloads)]>>(Rating >= RatingTh, Downloads =< 5000), AppList, FilteredApps),
    sort(2, @>=, FilteredApps, SortedApps),
    take(N, SortedApps, TopApps).

% Predicato per trovare N app di successo e con valutazione superiore o uguale a un certo valore ordinate per download
top_apps_by_rating(RatingTh, N, TopApps) :-
    findall((AppName, Downloads, Rating), (app_success_rating_downloads(AppName, 'Very popular', Rating, Downloads), Rating >= RatingTh), AppsWithRating),
    sort(2, @>=, AppsWithRating, SortedAppsWithRating),
    maplist([Tuple, NewTuple]>>(Tuple = (A,IntegerB,C), atom_string(IntegerB, StringB), NewTuple = (A,StringB,C)), SortedAppsWithRating, ConvertedList),
    take(N, ConvertedList, TopApps).

% Predicato per ottenere una lista di N app sotto una certa soglia di prezzo e di una certa categoria
apps_by_category_price(Category, PriceTh, N, TopApps) :- 
    findall((AppName, Price), (app_category_price(AppName, Category, Price), Price =< PriceTh), List),
    sort(2, @=<, List, SortedList),
    take(N, SortedList, TopApps).

% Predicato che conta il numero di app di una specifica categoria che sono editor choice
count_editors_choice(Category, Count) :- 
    findall(AppName, app_category_edchoice(AppName, Category, 'True'), List),
    length(List, Count).
    
% Predicato che restituisce una lista di N app di una specifica categoria che sono editor choice e ordinate per download
top_editors_choice(Category, N, AppList) :- 
    findall((AppName, Downloads), app_category_edchoice_downloads(AppName, Category, 'True', Downloads), List),
    sort(2, @>=, List, SortedList),
    take(N, SortedList, AppList).

% Predicato che restituisce una lista di N app di una specifica categoria ordinate per numero di download
top_downloads_by_category(Category, N, AppList) :- 
    findall((AppName, Downloads), app_category_downloads(AppName, Category, Downloads), List),
    sort(2, @>=, List, SortedList),
    take(N, SortedList, AppList).

% Predicato che effettua la somma dei download per una categoria specifica
sum_downloads_by_category(Category, TotalDownloads) :-
    findall(Downloads, app_category_downloads(_, Category, Downloads), DownloadList),
    sumlist(DownloadList, TotalDownloads).
    
% Predicato che ordina le categorie per numero totale di downloads
categories_ranked_by_downloads(TotalDownloadsList) :-
    findall(Category, app_category(_, Category), Categories),
    list_to_set(Categories, UniqueCategories),
    findall((Category, TotalDownloads), (member(Category, UniqueCategories), sum_downloads_by_category(Category, TotalDownloads)), List),
    sort(2, @>=, List, SortedList),
    maplist([Tuple, NewTuple]>>(Tuple = (A,IntegerB), atom_string(IntegerB, StringB), NewTuple = (A,StringB)), SortedList, TotalDownloadsList).

% Predicato che calcola il rating medio per una categoria specifica
avg_rating_by_category(Category, AvgRating) :-
    findall(Rating, app_category_rating(_, Category, Rating), RatingList),
    sumlist(RatingList, TotalRating),
    length(RatingList, N),
    AvgRatingRaw is TotalRating / N,
    format(atom(AvgRatingAtom), '~2f', [AvgRatingRaw]),
    atom_number(AvgRatingAtom, AvgRating).
    
% Predicato che calcola i download medi di una categoria specifica
avg_downloads_by_category(Category, AvgDownloads) :-
    findall(Downloads, app_category_downloads(_, Category, Downloads), DownloadList),
    sumlist(DownloadList, TotalDownloads),
    length(DownloadList, N),
    AvgDownloadsRaw is TotalDownloads / N,
    format(atom(AvgDownloadsAtom), '~0f', [AvgDownloadsRaw]),
    atom_number(AvgDownloadsAtom, AvgDownloads).

% Predicato che ordina le categorie per rating medio
categories_ranked_by_rating(TotalRatingList) :-
    findall(Category, app_category(_, Category), Categories),
    list_to_set(Categories, UniqueCategories),
    findall((Category, AvgRating), (member(Category, UniqueCategories), avg_rating_by_category(Category, AvgRating)), List),
    sort(2, @>=, List, TotalRatingList).

% Predicato che restituisce una lista di N app più costose con maggior numero di download
top_expensive_downloads(N, SortedByDownloads) :-
    findall((AppName, Price, Downloads), app_price_downloads(AppName, Price, Downloads), List),
    sort(2, @>=, List, SortedByPrice),
    take(N, SortedByPrice, TopApps),
    maplist([Tuple, ReversedTuple]>>(Tuple = (A,B,C), ReversedTuple = (A,C,B)), TopApps, ReversedList),
    sort(2, @>=, ReversedList, SortedByDownloads).

% Predicato che trova le app gratuite con maggior numero di download
top_free_downloads(N, TopApps) :-
    findall((AppName, Downloads), app_price_downloads(AppName, 0.0, Downloads), AppList),
    sort(2, @>=, AppList, SortedList),
    % Trasforma Downloads in stringa con atom_string
    maplist([Tuple, NewTuple]>>(Tuple = (A,IntegerB), atom_string(IntegerB, StringB), NewTuple = (A,StringB)), SortedList, ConvertedList),
    take(N, ConvertedList, TopApps).
    
% Predicato che restituisce la lista degli sviluppatori con più app di successo in una categoria
top_developers_by_success(Category, N, TopDevList) :-
    findall(Dev, app_category_developer_success(_, Category, Dev, 'Very popular'), Devs),
    msort(Devs, SortedDevs),
    bagof((Dev, Count), (member(Dev, SortedDevs), count_occurrences(Dev, SortedDevs, Count)), DevCountList),
    list_to_set(DevCountList, DevCountUniqueList),
    sort(2, @>=, DevCountUniqueList, SortedDevCountList),
    take(N, SortedDevCountList, TopDevList).
"""

write_rules(rules)
