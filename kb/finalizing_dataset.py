import os
import pandas as pd
from pyswip import Prolog
from kb.use_kb import query

df = pd.read_csv('../dataset/balanced-playstore-apps.csv', na_filter=False)
current_dir = os.path.dirname(__file__)
facts_path = os.path.join(current_dir, "facts.pl").replace("\\", "/")
rules_path = os.path.join(current_dir, "rules.pl").replace("\\", "/")

prolog = Prolog()
prolog.consult(facts_path)
prolog.consult(rules_path)

df_new = pd.DataFrame(columns=['Category', 'Num Apps by Developer', 'Num Editors Choice in Category',
                               'Total Downloads in Category', 'Average Downloads in Category',
                               'Average Rating of Category'])
df_new['Category'] = df['Category'].copy()

for cat in df_new['Category']:
    count_edc = query(prolog, f"count_editors_choice('{cat}', Count)")
    cat_avg_downloads = query(prolog, f"avg_downloads_by_category('{cat}', Count)")
    cat_avg_rating = query(prolog, f"avg_rating_by_category('{cat}', Count)")

    df_new.loc[df['Category'] == cat, 'Num Editors Choice in Category'] = count_edc[0]['Count']
    df_new.loc[df['Category'] == cat, 'Average Downloads in Category'] = cat_avg_downloads[0]['Count']
    df_new.loc[df['Category'] == cat, 'Average Rating of Category'] = cat_avg_rating[0]['Count']

df.insert(df.columns.get_loc('Success Rate'), 'Num Editors Choice in Category', df_new['Num Editors Choice in Category'])
df.insert(df.columns.get_loc('Success Rate'), 'Average Downloads in Category', df_new['Average Downloads in Category'])
df.insert(df.columns.get_loc('Success Rate'), 'Average Rating of Category', df_new['Average Rating of Category'])

df.to_csv('../dataset/finalized-playstore-apps.csv', index=False)
