import pandas as pd

from db_conect import DBConn
from extrator import DataSet
# from tratador import DataSetTable
from tqdm import tqdm
from driver_chrome import Chrome
import os

from to_db import DBQuerie
from tratador import Trat


def lixa(driver=None, ini=1, max_pg=50, sort='hotness'):
    return pd.concat(DataSet(pag=x, drive=driver, ordem=sort, save_backup=True).dataframe for x in range(ini, max_pg+1))







bd = DBConn()
# driver = Chrome()
# treino = lixa(driver=driver, max_pg=2)
# opcoes = lixa(driver=driver, sort='updated', max_pg=2)
# driver.bye()


df = Trat('hotness', bd.conn)
df2 = Trat('updated', bd.conn)
# slq = DBQuerie(conect)
qye = '?'


