import datetime
import numpy as np
import pyupbit
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
import FinanceDataReader as fdr
import pandas_datareader as pdr
import make_indicator


# db_file = "D:/db_files/data.db"
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()
# # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tickers = ['코스피100','코스피200','다우존스']
# lines = ['ma5','close','ma20']
# df = pd.DataFrame()
# for i, ticker in enumerate(tickers):
#     line = lines[i]
#     df_ticker = pd.read_sql("SELECT * FROM " + "'" + ticker + "'", conn).set_index('index')
#     s = df_ticker[line]
#     s.rename(f'{ticker}_{line}',inplace=True) #시리즈의 컬럼명 변경
#     df = pd.concat([df, s],axis=1)
# conn.close()
# print(df)
# save_file = "D:/db_files/save.db"
# stocks = fdr.StockListing('NYSE')
# KOSPI_list = pd.DataFrame({'종목코드': stock.get_market_ticker_list(market="KOSPI")})
# print(KOSPI_list)
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("texteditTest.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.fontSize = 10

        #TextEdit과 관련된 버튼에 기능 연결
        self.btn_printTextEdit.clicked.connect(self.printTextEdit)
        self.btn_clearTextEdit.clicked.connect(self.clearTextEdit)
        self.btn_setFont.clicked.connect(self.setFont)
        self.btn_setFontItalic.clicked.connect(self.fontItalic)
        self.btn_setFontColor.clicked.connect(self.fontColorRed)
        self.btn_fontSizeUp.clicked.connect(self.fontSizeUp)
        self.btn_fontSizeDown.clicked.connect(self.fontSizeDown)

    def printTextEdit(self) :
        print(self.textedit_Test.toPlainText())

    def clearTextEdit(self) :
        self.textedit_Test.clear()

    def setFont(self) :
        fontvar = QFont("Apple SD Gothic Neo",10)
        self.textedit_Test.setCurrentFont(fontvar)

    def fontItalic(self) :
        self.textedit_Test.setFontItalic(True)

    def fontColorRed(self) :
        colorvar = QColor(255,0,0)
        self.textedit_Test.setTextColor(colorvar)

    def fontSizeUp(self) :
        self.fontSize = self.fontSize + 1
        self.textedit_Test.setFontPointSize(self.fontSize)

    def fontSizeDown(self) :
        self.fontSize = self.fontSize - 1
        self.textedit_Test.setFontPointSize(self.fontSize)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
