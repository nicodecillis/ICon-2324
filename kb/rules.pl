
% Predicato per restituire i primi N elementi di una lista
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
    Elem \= Head,
    count_occurrences(Elem, Tail, Count).

% Predicato per trovare le app di uno specifico sviluppatore
apps_by_developer(Dev, AppName) :- app_developer(AppName, Dev).
apps_by_developer_list(Dev, List) :- 
    findall(AppName, apps_by_developer(Dev, AppName), List).
    
% Predicato per ottenere una lista di N app entro una certa soglia di prezzo e con una valutazione superiore o uguale a un certo valore
top_rating_price(RatingTh, PriceTh, N, TopApps) :- 
    findall((AppName, Rating, Price), (app_rating_price(AppName, Rating, Price), Price =< PriceTh, Rating >= RatingTh), AppList),
    sort(2, @>=, AppList, SortedApps),
    take(N, SortedApps, TopApps).

% Predicato per ottenere una lista di N app ordinate per numero di download per uno sviluppatore dato
top_downloads_by_developer(Dev, N, TopAppsWithDownloads) :-
    findall((AppName, Downloads), app_developer_downloads(AppName, Dev, Downloads), AppsWithDownloads),
    sort(2, @>=, AppsWithDownloads, SortedAppsWithDownloads),
    take(N, SortedAppsWithDownloads, TopAppsWithDownloads).
    
% Predicato per ottenere una lista di N app con rating maggiore o uguale ad un certo valore ma poco scaricate
top_rating_low_downloads(RatingTh, N, TopApps) :-
    findall((AppName, Rating, Downloads), app_rating_downloads(AppName, Rating, Downloads), AppList),
    include([(_, Rating, Downloads)]>>(Rating >= RatingTh, Downloads =< 5000), AppList, FilteredApps),
    sort(2, @>=, FilteredApps, SortedApps),
    take(N, SortedApps, TopApps).

% Predicato per trovare app con valutazione superiore o uguale a un certo valore e molto scaricate
apps_by_rating_downloads_high(RatingTh, DownloadsTh, AppName) :- 
    app_rating_downloads(AppName, Rating, Downloads), Rating >= RatingTh, Downloads > DownloadsTh.

% Predicato per ottenere una lista di N app sotto una certa soglia di prezzo e di una certa categoria
apps_by_category_price(Category, PriceTh, N, TopApps) :- 
    findall((AppName, Price), (app_category_price(AppName, Category, Price), Price =< PriceTh), List),
    sort(2, @=<, List, SortedList),
    take(N, SortedList, TopApps).

% Predicato che conta il numero di app di una specifica categoria che sono editor choice
count_editors_choice(Category, Count) :- 
    findall(AppName, app_category_edchoice(AppName, Category, 'True'), List),
    length(List, Count).
    
% Predicato che restituisce una lista di N app di una specifica categoria che sono editor choice
top_editors_choice(Category, N, AppList) :- 
    findall(AppName, app_category_edchoice(AppName, Category, 'True'), List),
    take(N, List, AppList).

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
    sort(2, @>=, List, TotalDownloadsList).

% Predicato che calcola il rating medio per una categoria specifica
avg_rating_by_category(Category, AvgRating) :-
    findall(Rating, app_category_rating(_, Category, Rating), RatingList),
    sumlist(RatingList, TotalRating),
    length(RatingList, N),
    AvgRatingRaw is TotalRating / N,
    format(atom(AvgRatingAtom), '~2f', [AvgRatingRaw]),
    atom_number(AvgRatingAtom, AvgRating).

% Predicato che ordina le categorie per rating medio
categories_ranked_by_rating(TotalRatingList) :-
    findall(Category, app_category(_, Category), Categories),
    list_to_set(Categories, UniqueCategories),
    findall((Category, AvgRating), (member(Category, UniqueCategories), avg_rating_by_category(Category, AvgRating)), List),
    sort(2, @>=, List, TotalRatingList).

% Predicato che restituisce una lista di N app più costose con maggior numero di download
top_price_downloads(N, SortedByDownloads) :-
    findall((AppName, Price, Downloads), app_price_downloads(AppName, Price, Downloads), List),
    sort(2, @>=, List, SortedByPrice),
    take(N, SortedByPrice, TopApps),
    maplist([Tuple, ReversedTuple]>>(Tuple = (A,B,C), ReversedTuple = (A,C,B)), TopApps, ReversedList),
    sort(2, @>=, ReversedList, SortedByDownloads).

% Predicato che trova le app gratuite con maggior numero di download
top_free_downloads(N, TopApps) :-
    findall((AppName, Downloads), app_price_downloads(AppName, 0.0, Downloads), List),
    sort(2, @>=, List, SortedList),
    take(N, SortedList, TopApps).
    
% Predicato che restituisce la lista degli sviluppatori con più app di successo in una categoria
top_developers_by_success(Category, N, TopDevList) :-
    findall(Dev, app_category_developer_success(_, Category, Dev, 'Very popular'), Devs),
    msort(Devs, SortedDevs),
    bagof((Dev, Count), (member(Dev, SortedDevs), count_occurrences(Dev, SortedDevs, Count)), DevCountList),
    list_to_set(DevCountList, DevCountUniqueList),
    sort(2, @>=, DevCountUniqueList, SortedDevCountList),
    take(N, SortedDevCountList, TopDevList).
    
% Predicato che restituisce una lista di app più di successo, con acquisti in app e ordinate per numero di download
top_success_purchases_downloads(N, TopApps) :-
    findall((AppName, Downloads), app_success_purchases_downloads(AppName, 'Very popular', 'True', Downloads), List),
    sort(2, @>=, List, SortedList),
    take(N, SortedList, TopApps).
    
% Predicato che restituisce la lista di app più di successo senza pubblicità e ordinate per download 
top_success_ad_downloads(N, TopApps) :-
    findall((AppName, Downloads), app_success_ad_downloads(AppName, 'Very popular', 'False', Downloads), List),
    sort(2, @>=, List, SortedList),
    take(N, SortedList, TopApps).
