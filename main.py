from db_conect import DBConn
from extrator import DataSet
# from tratador import DataSetTable
from tqdm import tqdm
from driver_chrome import Chrome
import os

from to_db import DBQuerie
from tratador import Trat


def lixa(driver=None, ini=1, max_pg=50, sort='hotness'):
    for x in tqdm(range(ini, max_pg+1), desc='main'):
        DataSet(pag=x, drive=driver, ordem=sort)







driver = Chrome()
lixa(driver=driver)
lixa(driver=driver, sort='updated')
driver.bye()

bd = DBConn()
conect = bd.conn
df = Trat('hotness', conect)
df = Trat('updated', conect)
# slq = DBQuerie(conect)
qye = '?'


