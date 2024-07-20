# da togliere in use_kb
def print_categories(categories):
    print("Le categorie disponibili sono:")
    for c in categories:
        print("- ", c)


def print_content_ratings(content_ratings):
    print("Le app si classificano sulla base dei contenuti in:")
    for r in content_ratings:
        print("- ", r)


def normalization(min, max, value):
    return (value - min) / (max - min)


def calculate_success(rating, downloads):
    return (rating + downloads) / 2


def find_min_max():
    min_download = 1000
    max_download = 74000000

    min_rating = 0
    max_rating = 4.6

    return min_download, max_download, min_rating, max_rating


def calculate_norm_success(downloads, rating):
    min_download, max_download, min_rating, max_rating = find_min_max()

    normalized_downloads = normalization(min_download, max_download, downloads)
    normalized_rating = normalization(min_rating, max_rating, rating)
    success = calculate_success(normalized_rating, normalized_downloads)

    return round(success, 1) * 10


def add_success_rate_in_rows(df):
    min_download, max_download, min_rating, max_rating = find_min_max()

    for index, row in df.iterrows():
        downloads = min(row['Downloads'], max_download)
        rating = min(row['Rating'], max_rating)

        success = calculate_norm_success(downloads, rating)
        df.at[index, 'Success Rate'] = success


def convert_success_rate(success_rate):
    if 0 <= success_rate <= 3:
        return "1"
    elif success_rate == 4:
        return "2"
    elif success_rate == 5 or success_rate == 6:
        return "3"
    else:
        return "4"
