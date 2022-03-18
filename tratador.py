import json
from functools import reduce
import pandas as pd
import os
from extrator import DataSet



class Trat:

    def __init__(self, name, conn, df=None):
        if not df:
            df = pd.concat([pd.read_csv(f'data/dataset/{csv}')
                                    for csv in os.listdir('data/dataset')
                                        if f'sort={name}' in csv],
                          ignore_index=True).drop('Unnamed: 0', axis=1).dropna(how='all')

        self.df = df.reset_index().rename(columns={'index': 'id'})
        self.df.Views = self.df.Views.apply(self.numero)
        self.df.Downloads = self.df.Downloads.apply(self.numero)
        self.df.tamanho = self.df.tamanho.apply(self.numerobi)
        self.df['Notebook Upvotes'] = self.df['Notebook Upvotes'].apply(self.numero)

        self.df.tags = self.df.tags.apply(self.tagnha)
        
        self.df_tags = self.df[['id', 'tags']].explode('tags')

        print('tratatin')

        self.df.to_sql(f'{name}', conn, if_exists='replace', index=False)



    def numero(self, num):
        if isinstance(num, (int, float)):
            return num
        if num.endswith('k'):
            return int(float(num[:-1]) * 10 ** 3)
        elif num.endswith('m'):
            return int(float(num[:-1]) * 10 ** 6)
        return int(num)


    def numerobi(self, num):
        num = num.lower()
        if num.endswith('b'):
            return float(num[:-2])
        elif num.endswith('kb'):
            return float(num[:-3]) * 10 ** 3
        elif num.endswith('mb'):
            return float(num[:-3]) * 10 ** 6
        elif num.endswith('gb'):
            return float(num[:-3]) * 10 ** 9


    def tagnha(self, lista):
        res = []
        if lista == 'No tags yet':
            res.append('No Tag')
        else:
            for x, y in eval(lista):
                res.append(x)
        return res



if __name__ == '__main__':

    d = Trat()

    que =32123
