import pandas as pd

df = pd.read_csv('../dataset/preprocessed-playstore-apps.csv', na_filter=False)

# RAGGRUPPAMENTO in quattro classi di Success Rate
df['Success Rate'] = df['Success Rate'].replace([0, 1, 2, 3], 1)
df['Success Rate'] = df['Success Rate'].replace([4], 2)
df['Success Rate'] = df['Success Rate'].replace([5, 6], 3)
df['Success Rate'] = df['Success Rate'].replace([7, 8, 9, 10], 4)

# UNDERSAMPLING: Success Rate 1-3
success_min = 1
success_max = 3
min_samples = 50000

for success in range(success_min, success_max+1):
    sample = (df[(df['Success Rate'] == success)].sample(n=min_samples, random_state=42))
    df = df.drop(df[(df['Success Rate'] == success) & (~df['App Id'].isin(sample['App Id']))].index)
print("Numero di campioni totali dopo l'undersampling: ", len(df))

# OVERSAMPLING: Success Rate 4
min_samples = int(min_samples/2)
sample = (df[(df['Success Rate'] == 4)].sample(n=min_samples-len(df[(df['Success Rate'] == 4)]), replace=True, random_state=42))
df = pd.concat([df, sample])
print("Numero di campioni totali dopo l'oversampling: ", len(df))

df['Success Rate'] = df['Success Rate'].replace([1], 'Not very popular')
df['Success Rate'] = df['Success Rate'].replace([2], 'Mildly popular')
df['Success Rate'] = df['Success Rate'].replace([3], 'Popular')
df['Success Rate'] = df['Success Rate'].replace([4], 'Very popular')

df.to_csv('dataset/balanced-playstore-apps.csv', index=False)
