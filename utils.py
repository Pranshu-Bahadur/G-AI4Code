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
    def __init__(self, rootdir : str, fextstr : str = "**/*.*"):
        super().__init__(rootdir)

        self.jsons = self.fext('json')
        self.csvs = self.fext('csv')

        # get dist?




        
        #test = eval(open(DataFrame(self.meta['fpaths_df'].groupby(0)).to_dict()[1][1].iloc[0]['Path'], 'r').read())

        #test = DataFrame(test)

        #print(test)





ADataset("/home/verus-carver/Documents/code/datasets/AI4Code")


