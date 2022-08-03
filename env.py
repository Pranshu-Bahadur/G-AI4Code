exec(open('utils.py', 'r').read())

AI4CodeDataset('dataset.json')[0]


"""
ftrain_df['id'] = ftrain_df.index.to_series().apply(lambda x: x.split('.')[0])

ftrain_df.index = Index(list(range(1, ftrain_df.index.size + 1)))

#ftrain_df['fsource'] = ftrain_df.pop('Path').apply(lambda x: read_json(str(x)))

train_csvs = dsdir_df[dsdir_df.index.to_series().str.contains('train')]

train_csvs['fsource'] = train_csvs['Path'].apply(lambda x: read_csv(str(x)))

train_csvs = merge(*train_csvs['fsource'].to_list(), on='id')

t_df = merge(ftrain_df, train_csvs, on='id')

print(t_df)
"""

