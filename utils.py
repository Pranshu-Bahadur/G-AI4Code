# Import Libraries
from pathlib import Path


def get_confs(rootdir : str, extstr : str = "**/*.json"):
    return list(Path(rootdir).glob(extstr))


LIBS = list(map(lambda x: eval(open(x, 'r').read()), get_confs("libs")))
exec('\n '.join(list(map(lambda x: ''.join(list(map(lambda k: f"from {k[0]} import {', '.join(k[1])}\n", x.items()))), LIBS))))

# ------


def scope_dir(rootdir : str, **kwargs):
    fdirdf = DataFrame(get_confs(rootdir, **kwargs), columns=['Path'])
    fdirdf.index = fdirdf['Path'].apply(lambda x : x.name).rename('fname')
    return fdirdf

def eval_file(fdirdf, fname : str) -> str:
    return open(fdirdf.loc[fname]['Path'], 'r').read()

"""

TODO(s):
    - [ ] better way to load tokenizer w/ [ ] tokenizer kwargs
    = [ ] rework getitem func

"""
class AI4CodeDataset(Dataset):
    def __init__(self, conf : str):
        super().__init__()

        self.conf = eval(eval_file(scope_dir('conf'), conf))
        substrs = self.conf.pop('substrs')

        types = ['code', 'markdown']

        self.tokenizers = dict(zip(types, list(map(lambda tokenizer : \
                AutoTokenizer.from_pretrained(tokenizer), list(self.conf.pop('tokenizers').values())))))

        list(map(lambda x : x.add_special_tokens({'pad_token': '[PAD]'}),self.tokenizers.values()))



        self.dir_df = scope_dir(**self.conf)
        
        t_df, train_df = self._split_df(substrs)
        
        t_df = merge(*t_df['Path'].apply(lambda x: \
                read_csv(x)).to_list(), on='id')

        train_df['id'] = train_df.index.to_series().apply(lambda x: x.split('.')[0])
        self.train_df = merge(train_df, t_df, on='id')
        self.train_df['labels'] = self.train_df.pop('cell_order').str.split(' ')


    def _split_df(self, substrs : list) -> dict:

        df = self.dir_df
        return tuple(list(map(lambda substr: df[df.index.to_series().str.contains(substr)], substrs)))


    def __getitem__(self, index : int):
        
        sample = self.train_df.iloc[index]
        sample['inputs'] = read_json(sample.pop('Path'))

        types = sample['inputs']['cell_type'].unique()
 
        y = DataFrame(sample.pop('labels'), columns=['id'])
        y['rank'] = y.index
        y.index = y.pop('id').values

        x = dict(zip(types, list(map(lambda label : sample['inputs'][sample['inputs']['cell_type'] == label], types))))
        y = {'code' : Tensor(y['rank'][x['code'].index].values), 'markdown': Tensor(y['rank'][x['markdown'].index].values)}

        sample = dict(zip(types, zip(y.values(), list(map(lambda kv:\
                self.tokenizers[kv[0]](kv[1]['source'].values.tolist(), truncation=True, padding=True, return_tensors="pt"), x.items())))))

        print(sample)
        return sample

