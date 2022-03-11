import pandas as pd
import os







class DBQuerie:

    def __init__(self, conn, path='data/dataset'):
        self.conect = conn
        self.hotness = pd.concat([pd.read_csv(f'{path}/{csv}') for csv in os.listdir(path)
                                                                        if 'sort=hotness' in csv],
                                                ignore_index=True).drop('Unnamed: 0', axis=1).dropna(how='all')
        self.topg(self.hotness, 'hotness')

        self.updated = pd.concat([pd.read_csv(f'{path}/{csv}') for csv in os.listdir(path)
                                                                        if 'sort=updated' in csv],
                                                ignore_index=True).drop('Unnamed: 0', axis=1).dropna(how='all')
        self.topg(self.hotness, 'updated')

        self.tags = pd.read_csv('data/inputs/Tags.csv').to_sql('tags', self.conect, if_exists='replace', index=False)


    def topg(self, df, nome):
        df.to_sql(nome, self.conect, if_exists='replace', index=False)
        print(f'{nome} Salvo BB!')




if __name__ == '__main__':
    DBQuerie()

