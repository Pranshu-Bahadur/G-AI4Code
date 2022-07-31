from pathlib import Path
from pandas import DataFrame


def rootdir2Df(rootdir : str, fext : str = "**/*.*") -> DataFrame:
    return DataFrame(list(Path(rootdir).glob(fext)), columns=['Path'])

exec(open(''.join(rootdir2Df('libs').applymap(str)['Path'].values), 'r').read())

class Pathfinder(object):
    def __init__(self, rootdir : str, fextstr : str = "**/*.*"):
        df = rootdir2Df(rootdir)
        df = DataFrame(merge(df, df['Path'].apply(str).str.extract(r'.([a-z]{3,4}$)'), \
                right_index=True, left_index=True))

        self.meta = {
                'fpaths_df' : df
                }
class ADataset(Dataset, Pathfinder):
    def __init__(self, rootdir : str, fextstr : str = "**/*.*"):
        super().__init__(rootdir)
        print(self.meta)


ADataset("/home/verus-carver/Documents/code/datasets/AI4Code")


