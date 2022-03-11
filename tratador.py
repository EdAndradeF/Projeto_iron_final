import json
from functools import reduce

import pandas as pd
import os
from extrator import DataSet


# class DataSetTable:
#     pass
#     # def __init__(self):
#     #
#     #     '''
#     #         vai receber um objeto DataSet para limpeza e
#     #         preparacao antes da entrada no banco de dados sql
#     #
#     #     :param data_obj: objeto DataSet
#     #
#     #     '''
#     #
#     #     self.data = pd.concat([pd.read_csv(f'data/{x}') for x in os.listdir('data')], ignore_index=True)
#     #     self.test = self.data.tags.str.replace(r'\xa0', "', '", regex=False)
#     #     self.data.tags = self.data.tags.str.replace(r'\xa0', "', '", regex=False)
#     #     self.data.tags = self.data.tags.apply(self.trat_tag)
#     #
#     #     w = r'[\'exercise\\xa0exercisesubject \', \' health and fitness \', \' exercise\']'
#     #
#     #
#     def trat_tag(self, tag_list):
#         if tag_list == 'No tags yet':
#             return tag_list
#         tag, delet = tag_list.split('Edit Tags')
#         tags = eval(f"{tag}']")
#         lista = [tags[x].replace(tags[x-1].replace(',', ''), '') if tags[x-1].endswith(',') else tags[x].replace(tags[x-1], '') for x in range(1, len(tags))]
#         return ','.join(lista)
#
#
#
#


def tagnha(lista):
    res = []
    if lista == 'No tags yet':
        res.append(('No Tag'))
    else:
        for x, y in eval(lista):
            res.append(x)
    return res


class Trat:

    def __init__(self, name, conn):
        self.df = pd.concat([pd.read_csv(f'data/dataset/{csv}')
                                for csv in os.listdir('data/dataset')
                                    if f'sort={name}' in csv],
                      ignore_index=True).drop('Unnamed: 0', axis=1).dropna(how='all')

        self.df.Views = self.df.Views.apply(self.numero)
        self.df.Downloads = self.df.Downloads.apply(self.numero)
        self.df.tamanho = self.df.tamanho.apply(self.numerobi)
        self.df['Notebook Upvotes'] = self.df['Notebook Upvotes'].apply(self.numero)

        self.df.tags = self.df.tags.apply(tagnha)
        self.df = self.df.explode('tags')





        self.df.to_sql(f'{name}', conn, if_exists='replace', index=False)



        print('tratatin')
        paradinha = ''
        adad =12

    '3.33 kb'
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




if __name__ == '__main__':

    d = Trat()


    que =32123
