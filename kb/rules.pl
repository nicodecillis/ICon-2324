
% Predicato per restituire i primi N elementi di una lista
take(0, _, []).
take(N, [Head|Tail], [Head|Taken]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Tail, Taken).

% Predicato per trovare le app di uno specifico sviluppatore
apps_by_developer(Dev, AppName) :- app_developer(AppName, Dev).
apps_by_developer_list(Dev, List) :- 
    findall(AppName, apps_by_developer(Dev, AppName), List).
    
% Predicato per ottenere una lista (con AppName, Price, Rating) di N app entro una certa soglia di prezzo e con una valutazione superiore o uguale a un certo valore
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

% Regola per ottenere una lista di N app sotto una certa soglia di prezzo e di una certa categoria
apps_by_category_price(Category, PriceTh, N, TopApps) :- 
    findall((AppName, Price), (app_category_price(AppName, Category, Price), Price =< PriceTh), List),
    sort(2, @=<, List, SortedList),
    take(N, SortedList, TopApps).
