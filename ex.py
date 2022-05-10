import datetime
import numpy as np
from PyQt5.QtWidgets import *
import sqlite3
import pandas as pd
from pandas import Series
# pd.set_option('display.max_row',None) #모든 행을 보고자 할 때
pd.set_option('display.max_columns',None) #모든 열을 보고자 할 때
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width',1500)
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option('mode.chained_assignment',  None) # SettingWithCopyWarning 경고를 끈다
import numpy as np
import sys
import os.path
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSortFilterProxyModel,Qt
from PyQt5.QtWidgets import (QApplication, QTableWidget)
from collections import Counter
from pykrx import stock
from PyQt5.QtTest import QTest
import datetime

db_file = "D:/db_files/data.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tickers = ['코스피100','코스피200','다우존스']
lines = ['ma5','close','ma20']
df = pd.DataFrame()
graph = []
for i, ticker in enumerate(tickers):
    line = lines[i]
    df_ticker = pd.read_sql("SELECT * FROM " + "'" + ticker + "'", conn).set_index('index')
    s = df_ticker[line]
    s.rename(f'{ticker}_{line}',inplace=True) #시리즈의 컬럼명 변경
    graph.append(f'{ticker}_{line}')
    df = pd.concat([df, s],axis=1)
conn.close()
print(df)
print(graph)
con = sqlite3.connect("D:/db_files/save.db")
now=datetime.datetime.now()
df.to_sql(str(now),con)