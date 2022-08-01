from pathlib import Path
from pandas import DataFrame

def rootdir2Df(rootdir : str, fext : str = "**/*.*") -> DataFrame:
    return DataFrame(list(Path(rootdir).glob(fext)), columns=['Path'])

exec(open(''.join(rootdir2Df('libs').applymap(str)['Path'].values), 'r').read())

class Pathfinder(object):
    def __init__(self, rootdir : str, fextstr : str = "**/*.*"):
        self.df = rootdir2Df(rootdir)
        self.fext = lambda fextstr: self.df[self.df['Path'].apply(str).str.contains(fextstr)]

class ADataset(Dataset, Pathfinder):
    def __init__(self, rootdir : str, fextstr : str = "**/*.*", tokenizers : dict = {
        'code' : AutoTokenizer.from_pretrained("codeparrot/codeparrot"),
        'markdown': None
            }):
        super().__init__(rootdir)
        self.jsons = self.fext('json')
        self.csvs = self.fext('csv')

        self.jsons = merge(self.jsons, self.jsons.applymap(lambda x: x.name[:-5]), right_index=True, left_index=True)
        self.jsons = self.jsons.rename(columns={'Path_y' : 'id', 'Path_x' : 'abspath'})

        self.train = concat(DataFrame(merge(read_csv(self.csvs.iloc[0]['Path']), \
                self.jsons, on='id').fillna(0).groupby(['parent_id', 'ancestor_id']))[1].to_list())
        self.train = merge(read_csv(self.csvs.iloc[2]['Path']), self.train, on='id')
        
        self.tokenizers = tokenizers

        print(self.train)

    def __getitem__(self, index : int):
        sample = self.train.iloc[index].transpose()
        x = read_json(sample['abspath'])
        y = DataFrame(sample.pop('cell_order').split(' '), columns=['cell_id'])
        y['rank'] = y.index
        y.index = y.pop('cell_id')
        code_x = x['source'][x['cell_type'] == 'code'].apply(self.tokenizers['code'].encode)
        code_y = Tensor(y['rank'][code_x.index].values)

        return code_x, code_y
        

#print(ADataset("/home/verus-carver/Documents/code/datasets/AI4Code")[1])


