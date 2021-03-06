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
import crosshair
import make_indicator


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        # self.setGeometry(500, 100, 1000, 1000)
        # QTableWidget.setWindowTitle(self, "Custom table widget")
        proxymodel = QSortFilterProxyModel()  #정렬
        # self.table1 = QTableWidget()
        # self.table1.setMinimumSize(100, 500)
        # self.table1.setSortingEnabled(True) #정렬
        # self.table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) #더블클릭 시 수정 금지
        # self.table1.setModel(proxymodel)
        # self.configureTable1(self.table1)

        self.table2 = QTableWidget()
        self.table2.setSortingEnabled(True)
        self.table2.setMinimumSize(100, 100)
        self.table2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.configureTable2(self.table2)
        self.table3 = QTableWidget()
        self.table3.setMinimumSize(100, 150)
        self.table3.setSortingEnabled(True)
        self.table3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table4 = QTableWidget()
        self.table4.setMinimumSize(100,  50)
        self.table4.setSortingEnabled(True)
        self.table4.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table5 = QTableWidget()
        self.table5.setMinimumSize(100, 450)
        self.table5.setSortingEnabled(True)
        self.table5.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        #https://appia.tistory.com/276
        # https://hello-bryan.tistory.com/213
        self.btn1 = QPushButton('차트보기')
        self.btn1.clicked.connect(lambda: self.show_chart())
        self.btn2 = QPushButton('backtest')
        self.btn2.clicked.connect(lambda: self.configureTable2(self.table2))
        self.btn3 = QPushButton('backtest_최적화')
        self.btn3.clicked.connect(lambda: self.configureTable4(self.table4))


        self.holic_btn2 = QPushButton('차멍 / 끄기')
        self.holic_btn2.clicked.connect(lambda: self.holic_back(delay))
        self.holic_btn2.setCheckable(True)

        self.holic_btn3 = QPushButton('차멍 / 끄기')
        self.holic_btn3.clicked.connect(lambda: self.holic_vc(delay))
        self.holic_btn3.setCheckable(True)

        # https: // www.pythonguis.com / tutorials / pyqt - layouts /
        self.edit_start_1 = QLineEdit(self)
        self.edit_end_1 = QLineEdit(self)
        self.edit_start_2 = QLineEdit(self)
        self.edit_end_2 = QLineEdit(self)
        self.lbl_duration_1 = QLabel('Tab1 (예-20220512) : ')
        self.lbl_duration_2 = QLabel('Tab2: ')
        self.lbl_t = QLabel('~')
        self.ch_c_cap = QCheckBox('시총,주식수')
        self.ch_c_ohlcv = QCheckBox('시고저종')
        self.ch_c_fun = QCheckBox('지표')
        self.ch_r_cap = QCheckBox('시총,주식수')
        self.ch_r_ohlcv = QCheckBox('시고저종')
        self.ch_r_fun = QCheckBox('지표')
        # self.radio_ch1 = QRadioButton('거시경제')
        # self.radio_ch1.setChecked(True)
        # self.radio_ch2 = QRadioButton('국내주식')
        # self.radio_ch3 = QRadioButton('미국주식')
        self.edit1 = QLineEdit(self)
        self.edit2 = QLineEdit(self)
        self.edit3 = QLineEdit(self)
        self.edit4 = QLineEdit(self)
        self.edit5 = QLineEdit(self)
        self.edit6 = QLineEdit(self)
        self.edit7 = QLineEdit(self)
        self.lbl1 = QLabel('avg')
        self.edit1.setText('30') #초기값
        self.lbl2 = QLabel('체결강도')
        self.edit2.setText('80')
        self.lbl3 = QLabel('거래대금')
        self.edit3.setText('1500')
        self.lbl4 = QLabel('매도총잔량평균')
        self.edit4.setText('60000')
        self.lbl5 = QLabel('고저평균대비등락율')
        self.edit5.setText('0')
        self.lbl6 = QLabel('체결강도max')
        self.edit6.setText('500')
        self.lbl7 = QLabel('체결강도-체결강도평균')
        self.edit7.setText('5')


        # self.lbl_del = QLabel('백테삭제조건')
        # self.lbl_del_val = QLabel('백테삭제값')
        # self.btn_del = QPushButton('차멍 / 끄기')
        # self.btn_del.clicked.connect(lambda: self.holic_vc(delay))
        # self.btn_del.setCheckable(True)
        self.plain_db_list = QPlainTextEdit(self)
        self.plain_krx_list = QPlainTextEdit(self)
        self.plain_us_list = QPlainTextEdit(self)

        db_list, krx_list, us_list = self.db_list()
        self.plain_db_list.setPlainText(str(db_list))
        self.plain_krx_list.setPlainText(str(krx_list))
        self.plain_us_list.setPlainText(str(us_list))


        # self.edit1_t = self.edit1.text() #초기값을 전달
        # self.edit2_t = self.edit2.text() #초기값을 전달
        # self.edit3_t = self.edit3.text() #초기값을 전달
        # self.edit4_t = self.edit4.text() #초기값을 전달
        # self.edit5_t = self.edit5.text() #초기값을 전달
        # self.edit6_t = self.edit6.text() #초기값을 전달
        # self.edit7_t = self.edit7.text() #초기값을 전달

        self.edit1.textChanged[str].connect(self.val_change)
        self.edit2.textChanged[str].connect(self.val_change)
        self.edit3.textChanged[str].connect(self.val_change)
        self.edit4.textChanged[str].connect(self.val_change)
        self.edit5.textChanged[str].connect(self.val_change)
        self.edit6.textChanged[str].connect(self.val_change)
        self.edit7.textChanged[str].connect(self.val_change)

        # self.spinbox1.setRange(0, 200)
        # self.spinbox1.setSingleStep(1)
        # self.spinbox1.setValue(80)

        self.grid_top = QGridLayout(self)
        self.grid_top.setSpacing(10)
        # self.grid_top.addWidget(self.radio_ch1,0,0)
        # self.grid_top.addWidget(self.radio_ch2,1,0)
        # self.grid_top.addWidget(self.radio_ch3,2,0)
        self.grid_top.addWidget(self.lbl1,0,1)
        self.grid_top.addWidget(self.edit1,1,1)
        self.grid_top.addWidget(self.lbl2,0,2)
        self.grid_top.addWidget(self.edit2,1,2)
        self.grid_top.addWidget(self.lbl3,0,3)
        self.grid_top.addWidget(self.edit3,1,3)
        self.grid_top.addWidget(self.lbl4,0,4)
        self.grid_top.addWidget(self.edit4,1,4)
        self.grid_top.addWidget(self.lbl5,0,5)
        self.grid_top.addWidget(self.edit5,1,5)
        self.grid_top.addWidget(self.lbl6,0,6)
        self.grid_top.addWidget(self.edit6,1,6)
        self.grid_top.addWidget(self.lbl7,0,7)
        self.grid_top.addWidget(self.edit7,1,7)
        self.grid_top.addWidget(self.lbl_duration_1,0,8)
        self.grid_top.addWidget(self.edit_start_1,0,9)
        self.grid_top.addWidget(self.lbl_t,0,10)
        self.grid_top.addWidget(self.edit_end_1,0,11)
        self.grid_top.addWidget(self.lbl_duration_2,1,8)
        self.grid_top.addWidget(self.edit_start_2,1,9)
        self.grid_top.addWidget(self.lbl_t,1,10)
        self.grid_top.addWidget(self.edit_end_2,1,11)
        self.grid_top.addWidget(self.btn1,1,12)
        self.box_chart1 = QVBoxLayout(self)
        self.box_chart2 = QVBoxLayout(self)
        self.box_bt_list = QVBoxLayout(self)
        self.box_bt_detail = QVBoxLayout(self)
        self.box_db_list = QVBoxLayout(self)
        self.box_krx_list = QVBoxLayout(self)
        self.box_us_list = QVBoxLayout(self)
        # self.box_luu = QHBoxLayout(self)
        self.box_cuu = QHBoxLayout(self)
        # self.box_ruu = QHBoxLayout(self)



        self.init_QLineEdit()


        self.grid_chart1 = QGridLayout(self)
        self.grid_chart1.setSpacing(10)
        self.grid_chart2 = QGridLayout(self)
        self.grid_chart2.setSpacing(10)
        self.init_grid()
        self.import_name()


        # self.box_luu.addWidget(self.lbl_duration_1)
        # self.box_luu.addWidget(self.edit_start_1)
        # self.box_luu.addWidget(self.lbl_t)
        # self.box_luu.addWidget(self.edit_end_1)
        # self.box_luu.addWidget(self.btn1)
        # self.box_chart1.addLayout(self.box_luu)
        self.box_db_list.addWidget(self.plain_db_list)
        self.box_krx_list.addWidget(self.plain_krx_list)
        self.box_us_list.addWidget(self.plain_us_list)
        self.box_chart1.addLayout(self.grid_chart1)
        # self.box_chart2.addLayout(self.box_luu)
        self.box_chart2.addLayout(self.grid_chart2)
        # self.box_chart1.addWidget(self.holic_btn1)
        self.box_cuu.addWidget(self.ch_c_cap)
        self.box_cuu.addWidget(self.ch_c_ohlcv)
        self.box_cuu.addWidget(self.ch_c_fun)
        self.box_cuu.addWidget(self.btn2)
        self.box_bt_list.addLayout(self.box_cuu)
        self.box_bt_list.addWidget(self.table2)
        self.box_bt_detail.addWidget(self.table3)
        self.box_bt_detail.addWidget(self.holic_btn2)
        # self.box_ruu.addWidget(self.ch_r_cap)
        # self.box_ruu.addWidget(self.ch_r_ohlcv)
        # self.box_ruu.addWidget(self.ch_r_fun)
        # self.box_ruu.addWidget(self.btn3)
        # self.box_ru.addLayout(self.box_ruu)
        # self.box_ru.addWidget(self.table4)
        # self.box_rd.addWidget(self.table5)
        # self.box_rd.addWidget(self.holic_btn3)

        self.frame_up = QFrame()
        self.frame_up.setMaximumSize(10000,  80)
        self.frame_up.setFrameShape(QFrame.StyledPanel)
        self.frame_up.setLayout(self.grid_top)

        self.frame_chart1 = QFrame()
        self.frame_chart1.setMinimumSize(900,550)
        self.frame_chart1.setFrameShape(QFrame.StyledPanel)
        self.frame_chart1.setLayout(self.box_chart1)

        self.frame_chart2 = QFrame()
        self.frame_chart2.setMinimumSize(900,550)
        self.frame_chart2.setFrameShape(QFrame.StyledPanel)
        self.frame_chart2.setLayout(self.box_chart2)

        self.frame_vj_list = QFrame()
        # self.frame_vj_list.setFixedSize(900,100)
        self.frame_vj_list.setFrameShape(QFrame.StyledPanel)
        self.frame_vj_list.setLayout(self.box_bt_list)

        self.frame_vj_detail = QFrame()
        # self.frame_vj_detail.setFixedSize(900,250)
        self.frame_vj_detail.setFrameShape(QFrame.StyledPanel)
        self.frame_vj_detail.setLayout(self.box_bt_detail)

        # self.frame_buy_stg = QFrame()
        # self.frame_buy_stg.setFrameShape(QFrame.StyledPanel)
        # # self.frame_buy_stg.setLayout(self.plain_buy_stg)
        # self.frame_sell_stg = QFrame()
        # self.frame_sell_stg.setFrameShape(QFrame.StyledPanel)
        # # self.frame_sell_stg.setLayout(self.plain_sell_stg)
        # self.frame_range = QFrame()
        # self.frame_range.setFrameShape(QFrame.StyledPanel)


        self.split_vj = QSplitter(Qt.Vertical)
        self.split_vj.addWidget(self.frame_vj_list)
        self.split_vj.addWidget(self.frame_vj_detail)

        self.split_list = QSplitter(Qt.Vertical)
        self.split_list.addWidget(self.plain_db_list)
        self.split_list.addWidget(self.plain_krx_list)
        self.split_list.addWidget(self.plain_us_list)





        self.splitter_chart = QSplitter(Qt.Horizontal)
        self.splitter_chart.addWidget(self.frame_chart1)
        self.splitter_chart.addWidget(self.frame_chart2)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.split_vj)
        self.splitter.addWidget(self.split_list)
        # self.splitter.addWidget(self.split_stg)


        self.vbox = QVBoxLayout()
        # self.vbox.resize(1800,500)
        self.vbox.addWidget(self.frame_up)
        self.vbox.addWidget(self.splitter_chart)
        self.vbox.addWidget(self.splitter)

        self.setLayout(self.vbox)
        self.table2.cellDoubleClicked.connect(self.celldoubleclicked_event2)
        self.table3.cellDoubleClicked.connect(self.celldoubleclicked_event3)
        self.table4.cellDoubleClicked.connect(self.celldoubleclicked_event4)
        self.table5.cellDoubleClicked.connect(self.celldoubleclicked_event5)
        # self.table3.doubleClicked.connect(self.celldoubleclicked_event2)



    def configureTable2(self, table):
        table.setSortingEnabled(False)
        table.clear()
        select = 'vj'
        self.df2 = qtable_back_list(select)
        table.setRowCount(len(self.df2.index))
        table.setColumnCount(len(self.df2.columns))
        header = table.horizontalHeader()# 컬럼내용에따라 길이 자동조절

        for i in range(len(self.df2.columns)):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(self.df2.columns[i]))
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents) # 컬럼내용에따라 길이 자동조절
        # for i in range(len(self.df2.index)):
        #     table.setVerticalHeaderItem(i, QTableWidgetItem(str(self.df2.index[i])[5:10]))
        table.verticalHeader().setVisible(False) #인덱스 삭제

        for row in range(len(self.df2.index)):
            for column in range(len(self.df2.columns)):
                val = self.df2.iloc[row, column]
                if type(val) != str:
                    val = val.item()  # numpy.float 을 float으로 변환
                it = QTableWidgetItem()
                it.setData(Qt.DisplayRole, val)  # 정렬 시 문자형이 아닌 숫자크기로 바꿈
                table.setItem(row, column, it)
        table.horizontalHeader().setStretchLastSection(True)
        # table.verticalHeader().setStretchLastSection(True)
        table.setSortingEnabled(True) #소팅한 상태로 로딩 시 데이터가 이상해져 맨 앞과 뒤에 추가
    def configureTable3(self, table,vj_time):
        table.setSortingEnabled(False)
        table.clear()
        cap = self.ch_c_cap.isChecked()
        ohlcv = self.ch_c_ohlcv.isChecked()
        fun = self.ch_c_fun.isChecked()
        self.df3 = qtable_backtest(vj_time,cap,ohlcv,fun)
        # self.df3['매수시간'] = self.df3['매수시간'].astype(str)
        # self.df3['매수시간'] = self.df3['매수시간'].str[4:6]+'/'+self.df3['매수시간'].str[6:8]+' '+self.df3['매수시간'].str[8:10]+':'+self.df3['매수시간'].str[10:12]+':'+self.df3['매수시간'].str[12:14]
        # self.df3['매도시간'] = self.df3['매도시간'].astype(str)
        # self.df3['매도시간'] = self.df3['매도시간'].str[4:6]+'/'+self.df3['매도시간'].str[6:8]+' '+self.df3['매도시간'].str[8:10]+':'+self.df3['매도시간'].str[10:12]+':'+self.df3['매도시간'].str[12:14]
        table.setRowCount(len(self.df3.index))
        table.setColumnCount(len(self.df3.columns))
        header = table.horizontalHeader()# 컬럼내용에따라 길이 자동조절

        for i in range(len(self.df3.columns)):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(self.df3.columns[i]))
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents) # 컬럼내용에따라 길이 자동조절
        # for i in range(len(self.df3.index)):
        #     table.setVerticalHeaderItem(i, QTableWidgetItem(str(self.df3.index[i])[5:10]))
        table.verticalHeader().setVisible(False) #인덱스 삭제
        for row in range(len(self.df3.index)):
            for column in range(len(self.df3.columns)):
                val = self.df3.iloc[row, column]
                if type(val) != str:
                    val = val.item()  # numpy.float 을 int로 변환
                    # print(type(val))
                it = QTableWidgetItem()
                it.setData(Qt.DisplayRole, val)  # 정렬 시 문자형이 아닌 숫자크기로 바꿈
                table.setItem(row, column, it)
        # table.horizontalHeader().setStretchLastSection(True)
        # table.verticalHeader().setStretchLastSection(True)
        table.setSortingEnabled(True) #소팅한 상태로 로딩 시 데이터가 이상해져 맨 앞과 뒤에 추가
    def configureTable4(self, table):
        table.setSortingEnabled(False)
        table.clear()
        select = 'vc'
        self.df4 = qtable_back_list(select)
        table.setRowCount(len(self.df4.index))
        table.setColumnCount(len(self.df4.columns))
        header = table.horizontalHeader()# 컬럼내용에따라 길이 자동조절

        for i in range(len(self.df4.columns)):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(self.df4.columns[i]))
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents) # 컬럼내용에따라 길이 자동조절
        # for i in range(len(self.df4.index)):
        #     table.setVerticalHeaderItem(i, QTableWidgetItem(str(self.df4.index[i])[5:10]))
        table.verticalHeader().setVisible(False) #인덱스 삭제

        for row in range(len(self.df4.index)):
            for column in range(len(self.df4.columns)):
                val = self.df4.iloc[row, column]
                if type(val) != str:
                    val = val.item()  # numpy.float 을 float으로 변환
                it = QTableWidgetItem()
                it.setData(Qt.DisplayRole, val)  # 정렬 시 문자형이 아닌 숫자크기로 바꿈
                table.setItem(row, column, it)
        table.horizontalHeader().setStretchLastSection(True)
        # table.verticalHeader().setStretchLastSection(True)
        table.setSortingEnabled(True) #소팅한 상태로 로딩 시 데이터가 이상해져 맨 앞과 뒤에 추가
    def configureTable5(self, table,vc_time):
        table.setSortingEnabled(False)
        table.clear()
        cap = self.ch_r_cap.isChecked()
        ohlcv = self.ch_r_ohlcv.isChecked()
        fun = self.ch_r_fun.isChecked()
        self.df5 = qtable_backtest(vc_time,cap,ohlcv,fun)
        #매수도시간 보기 편하게
        # self.df5['매수시간'] = self.df5['매수시간'].astype(str)
        # self.df5['매수시간'] = self.df5['매수시간'].str[4:6]+'/'+self.df5['매수시간'].str[6:8]+' '+self.df5['매수시간'].str[8:10]+':'+self.df5['매수시간'].str[10:12]+':'+self.df5['매수시간'].str[12:14]
        # self.df5['매도시간'] = self.df5['매도시간'].astype(str)
        # self.df5['매도시간'] = self.df5['매도시간'].str[4:6]+'/'+self.df5['매도시간'].str[6:8]+' '+self.df5['매도시간'].str[8:10]+':'+self.df5['매도시간'].str[10:12]+':'+self.df5['매도시간'].str[12:14]
        # print(self.df5)
        table.setRowCount(len(self.df5.index))
        table.setColumnCount(len(self.df5.columns))
        header = table.horizontalHeader()# 컬럼내용에따라 길이 자동조절

        for i in range(len(self.df5.columns)):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(self.df5.columns[i]))
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents) # 컬럼내용에따라 길이 자동조절
        # for i in range(len(self.df5.index)):
        #     table.setVerticalHeaderItem(i, QTableWidgetItem(str(self.df5.index[i])[5:10]))
        table.verticalHeader().setVisible(False) #인덱스 삭제
        for row in range(len(self.df5.index)):
            for column in range(len(self.df5.columns)):
                val = self.df5.iloc[row, column]
                if type(val) != str:
                    val = val.item()  # numpy.float 을 int로 변환
                    # print(type(val))
                it = QTableWidgetItem()
                it.setData(Qt.DisplayRole, val)  # 정렬 시 문자형이 아닌 숫자크기로 바꿈
                table.setItem(row, column, it)
        # table.horizontalHeader().setStretchLastSection(True)
        # table.verticalHeader().setStretchLastSection(True)
        table.setSortingEnabled(True) #소팅한 상태로 로딩 시 데이터가 이상해져 맨 앞과 뒤에 추가
    def celldoubleclicked_event2(self):
        self.plain_buy_stg.clear()
        self.plain_sell_stg.clear()
        self.plain_range.clear()
        row = self.table2.currentRow()
        vj_time = self.df2.index[row]
        print('vj_time=',vj_time)
        buy_stg = self.df2.loc[vj_time,'매수전략']
        sell_stg = self.df2.loc[vj_time,'매도전략']
        self.plain_buy_stg.setPlainText(buy_stg)
        self.plain_sell_stg.setPlainText(sell_stg)
        self.configureTable3(self.table3,vj_time)
    def celldoubleclicked_event3(self):
        row = self.table3.currentRow()
        stock_code = self.table3.item(row, 0).text()
        # stock_code = item.text()
        date = self.table3.item(row, 8).text() #매수시간에서 짤라가지고 date생성(컬럼수 늘어날 경우 숫자 변경해야됨)
        date = str(date)[4:8]
        # date = str(date)[0:2]+str(date)[2:4]
        print(stock_code, date)
        df = get_data(stock_code, date, start, end, )
        stock_name = make_stock_name(stock_code)
        # print(df)
        df = df_add(df,self.edit1_t,self.edit6_t)
        df = df_backtest(stock_code, df,self.df3)
        # View_Chart = self.select_chart()
        self.chart = Chart(df, stock_name,stock_code, date,self.edit2_t,self.edit3_t,self.edit4_t,self.edit5_t,self.edit7_t)
        self.chart.setGeometry(0, 30, 3850, 1010)
        self.chart.show()
    def celldoubleclicked_event4(self):
        self.plain_buy_stg.clear()
        self.plain_sell_stg.clear()
        self.plain_range.clear()
        row = self.table4.currentRow()
        vc_time = self.df4.index[row]
        print('vc_time=',vc_time)
        buy_stg = self.df4.loc[vc_time,'매수전략']
        sell_stg = self.df4.loc[vc_time,'매도전략']
        range = self.df4.loc[vc_time,'범위설정']
        self.plain_buy_stg.setPlainText(buy_stg)
        self.plain_sell_stg.setPlainText(sell_stg)
        self.plain_range.setPlainText(range)
        self.configureTable5(self.table5,vc_time)
    def celldoubleclicked_event5(self):
        row = self.table5.currentRow()
        stock_code = self.table5.item(row, 0).text()
        # stock_code = item.text()
        date = self.table5.item(row, 8).text() #매수시간에서 짤라가지고 date생성(컬럼수 늘어날 경우 숫자 변경해야됨)
        date = str(date)[4:8]
        print(stock_code, date)
        df = get_data(stock_code, date, start, end, )
        stock_name = make_stock_name(stock_code)
        # print(df)
        df = df_add(df,self.edit1_t,self.edit6_t)
        df = df_backtest(stock_code, df,self.df5)
        # View_Chart = self.select_chart()
        self.chart = Chart(df, stock_name,stock_code, date,self.edit2_t,self.edit3_t,self.edit4_t,self.edit5_t,self.edit7_t)
        self.chart.setGeometry(0, 30, 3850, 1010)
        self.chart.show()
    def get_edit_text(self):
        duration_s = self.edit_start_1.text()
        duration_e = self.edit_end_1.text()
        ticker1_1_1=self.edit1_1_1.text()
        ticker1_2_1=self.edit1_2_1.text()
        ticker1_3_1=self.edit1_3_1.text()
        ticker1_4_1=self.edit1_4_1.text()
        ticker1_5_1=self.edit1_5_1.text()
        ticker2_1_1=self.edit2_1_1.text()
        ticker2_2_1=self.edit2_2_1.text()
        ticker2_3_1=self.edit2_3_1.text()
        ticker2_4_1=self.edit2_4_1.text()
        ticker2_5_1=self.edit2_5_1.text()
        ticker3_1_1=self.edit3_1_1.text()
        ticker3_2_1=self.edit3_2_1.text()
        ticker3_3_1=self.edit3_3_1.text()
        ticker3_4_1=self.edit3_4_1.text()
        ticker3_5_1=self.edit3_5_1.text()
        ticker4_1_1=self.edit4_1_1.text()
        ticker4_2_1=self.edit4_2_1.text()
        ticker4_3_1=self.edit4_3_1.text()
        ticker4_4_1=self.edit4_4_1.text()
        ticker4_5_1=self.edit4_5_1.text()
        ticker5_1_1=self.edit5_1_1.text()
        ticker5_2_1=self.edit5_2_1.text()
        ticker5_3_1=self.edit5_3_1.text()
        ticker5_4_1=self.edit5_4_1.text()
        ticker5_5_1=self.edit5_5_1.text()
        ticker6_1_1=self.edit6_1_1.text()
        ticker6_2_1=self.edit6_2_1.text()
        ticker6_3_1=self.edit6_3_1.text()
        ticker6_4_1=self.edit6_4_1.text()
        ticker6_5_1=self.edit6_5_1.text()
        ticker7_1_1=self.edit7_1_1.text()
        ticker7_2_1=self.edit7_2_1.text()
        ticker7_3_1=self.edit7_3_1.text()
        ticker7_4_1=self.edit7_4_1.text()
        ticker7_5_1=self.edit7_5_1.text()
        ticker8_1_1=self.edit8_1_1.text()
        ticker8_2_1=self.edit8_2_1.text()
        ticker8_3_1=self.edit8_3_1.text()
        ticker8_4_1=self.edit8_4_1.text()
        ticker8_5_1=self.edit8_5_1.text()
        ticker9_1_1=self.edit9_1_1.text()
        ticker9_2_1=self.edit9_2_1.text()
        ticker9_3_1=self.edit9_3_1.text()
        ticker9_4_1=self.edit9_4_1.text()
        ticker9_5_1=self.edit9_5_1.text()
        ticker10_1_1=self.edit10_1_1.text()
        ticker10_2_1=self.edit10_2_1.text()
        ticker10_3_1=self.edit10_3_1.text()
        ticker10_4_1=self.edit10_4_1.text()
        ticker10_5_1=self.edit10_5_1.text()
        ticker11_1_1=self.edit11_1_1.text()
        ticker11_2_1=self.edit11_2_1.text()
        ticker11_3_1=self.edit11_3_1.text()
        ticker11_4_1=self.edit11_4_1.text()
        ticker11_5_1=self.edit11_5_1.text()
        ticker12_1_1=self.edit12_1_1.text()
        ticker12_2_1=self.edit12_2_1.text()
        ticker12_3_1=self.edit12_3_1.text()
        ticker12_4_1=self.edit12_4_1.text()
        ticker12_5_1=self.edit12_5_1.text()

        ticker13_1_1=self.edit1_1_1_2.text()
        ticker13_2_1=self.edit1_2_1_2.text()
        ticker13_3_1=self.edit1_3_1_2.text()
        ticker13_4_1=self.edit1_4_1_2.text()
        ticker13_5_1=self.edit1_5_1_2.text()
        ticker14_1_1=self.edit2_1_1_2.text()
        ticker14_2_1=self.edit2_2_1_2.text()
        ticker14_3_1=self.edit2_3_1_2.text()
        ticker14_4_1=self.edit2_4_1_2.text()
        ticker14_5_1=self.edit2_5_1_2.text()
        ticker15_1_1=self.edit3_1_1_2.text()
        ticker15_2_1=self.edit3_2_1_2.text()
        ticker15_3_1=self.edit3_3_1_2.text()
        ticker15_4_1=self.edit3_4_1_2.text()
        ticker15_5_1=self.edit3_5_1_2.text()
        ticker16_1_1=self.edit4_1_1_2.text()
        ticker16_2_1=self.edit4_2_1_2.text()
        ticker16_3_1=self.edit4_3_1_2.text()
        ticker16_4_1=self.edit4_4_1_2.text()
        ticker16_5_1=self.edit4_5_1_2.text()
        ticker17_1_1=self.edit5_1_1_2.text()
        ticker17_2_1=self.edit5_2_1_2.text()
        ticker17_3_1=self.edit5_3_1_2.text()
        ticker17_4_1=self.edit5_4_1_2.text()
        ticker17_5_1=self.edit5_5_1_2.text()
        ticker18_1_1=self.edit6_1_1_2.text()
        ticker18_2_1=self.edit6_2_1_2.text()
        ticker18_3_1=self.edit6_3_1_2.text()
        ticker18_4_1=self.edit6_4_1_2.text()
        ticker18_5_1=self.edit6_5_1_2.text()
        ticker19_1_1=self.edit7_1_1_2.text()
        ticker19_2_1=self.edit7_2_1_2.text()
        ticker19_3_1=self.edit7_3_1_2.text()
        ticker19_4_1=self.edit7_4_1_2.text()
        ticker19_5_1=self.edit7_5_1_2.text()
        ticker20_1_1=self.edit8_1_1_2.text()
        ticker20_2_1=self.edit8_2_1_2.text()
        ticker20_3_1=self.edit8_3_1_2.text()
        ticker20_4_1=self.edit8_4_1_2.text()
        ticker20_5_1=self.edit8_5_1_2.text()
        ticker21_1_1=self.edit9_1_1_2.text()
        ticker21_2_1=self.edit9_2_1_2.text()
        ticker21_3_1=self.edit9_3_1_2.text()
        ticker21_4_1=self.edit9_4_1_2.text()
        ticker21_5_1=self.edit9_5_1_2.text()
        ticker22_1_1=self.edit10_1_1_2.text()
        ticker22_2_1=self.edit10_2_1_2.text()
        ticker22_3_1=self.edit10_3_1_2.text()
        ticker22_4_1=self.edit10_4_1_2.text()
        ticker22_5_1=self.edit10_5_1_2.text()
        ticker23_1_1=self.edit11_1_1_2.text()
        ticker23_2_1=self.edit11_2_1_2.text()
        ticker23_3_1=self.edit11_3_1_2.text()
        ticker23_4_1=self.edit11_4_1_2.text()
        ticker23_5_1=self.edit11_5_1_2.text()
        ticker24_1_1=self.edit12_1_1_2.text()
        ticker24_2_1=self.edit12_2_1_2.text()
        ticker24_3_1=self.edit12_3_1_2.text()
        ticker24_4_1=self.edit12_4_1_2.text()
        ticker24_5_1=self.edit12_5_1_2.text()


        line1_1_2=self.edit1_1_2.text()
        line1_2_2=self.edit1_2_2.text()
        line1_3_2=self.edit1_3_2.text()
        line1_4_2=self.edit1_4_2.text()
        line1_5_2=self.edit1_5_2.text()
        line2_1_2=self.edit2_1_2.text()
        line2_2_2=self.edit2_2_2.text()
        line2_3_2=self.edit2_3_2.text()
        line2_4_2=self.edit2_4_2.text()
        line2_5_2=self.edit2_5_2.text()
        line3_1_2=self.edit3_1_2.text()
        line3_2_2=self.edit3_2_2.text()
        line3_3_2=self.edit3_3_2.text()
        line3_4_2=self.edit3_4_2.text()
        line3_5_2=self.edit3_5_2.text()
        line4_1_2=self.edit4_1_2.text()
        line4_2_2=self.edit4_2_2.text()
        line4_3_2=self.edit4_3_2.text()
        line4_4_2=self.edit4_4_2.text()
        line4_5_2=self.edit4_5_2.text()
        line5_1_2=self.edit5_1_2.text()
        line5_2_2=self.edit5_2_2.text()
        line5_3_2=self.edit5_3_2.text()
        line5_4_2=self.edit5_4_2.text()
        line5_5_2=self.edit5_5_2.text()
        line6_1_2=self.edit6_1_2.text()
        line6_2_2=self.edit6_2_2.text()
        line6_3_2=self.edit6_3_2.text()
        line6_4_2=self.edit6_4_2.text()
        line6_5_2=self.edit6_5_2.text()
        line7_1_2=self.edit7_1_2.text()
        line7_2_2=self.edit7_2_2.text()
        line7_3_2=self.edit7_3_2.text()
        line7_4_2=self.edit7_4_2.text()
        line7_5_2=self.edit7_5_2.text()
        line8_1_2=self.edit8_1_2.text()
        line8_2_2=self.edit8_2_2.text()
        line8_3_2=self.edit8_3_2.text()
        line8_4_2=self.edit8_4_2.text()
        line8_5_2=self.edit8_5_2.text()
        line9_1_2=self.edit9_1_2.text()
        line9_2_2=self.edit9_2_2.text()
        line9_3_2=self.edit9_3_2.text()
        line9_4_2=self.edit9_4_2.text()
        line9_5_2=self.edit9_5_2.text()
        line10_1_2=self.edit10_1_2.text()
        line10_2_2=self.edit10_2_2.text()
        line10_3_2=self.edit10_3_2.text()
        line10_4_2=self.edit10_4_2.text()
        line10_5_2=self.edit10_5_2.text()
        line11_1_2=self.edit11_1_2.text()
        line11_2_2=self.edit11_2_2.text()
        line11_3_2=self.edit11_3_2.text()
        line11_4_2=self.edit11_4_2.text()
        line11_5_2=self.edit11_5_2.text()
        line12_1_2=self.edit12_1_2.text()
        line12_2_2=self.edit12_2_2.text()
        line12_3_2=self.edit12_3_2.text()
        line12_4_2=self.edit12_4_2.text()
        line12_5_2=self.edit12_5_2.text()

        line13_1_2=self.edit1_1_2_2.text()
        line13_2_2=self.edit1_2_2_2.text()
        line13_3_2=self.edit1_3_2_2.text()
        line13_4_2=self.edit1_4_2_2.text()
        line13_5_2=self.edit1_5_2_2.text()
        line14_1_2=self.edit2_1_2_2.text()
        line14_2_2=self.edit2_2_2_2.text()
        line14_3_2=self.edit2_3_2_2.text()
        line14_4_2=self.edit2_4_2_2.text()
        line14_5_2=self.edit2_5_2_2.text()
        line15_1_2=self.edit3_1_2_2.text()
        line15_2_2=self.edit3_2_2_2.text()
        line15_3_2=self.edit3_3_2_2.text()
        line15_4_2=self.edit3_4_2_2.text()
        line15_5_2=self.edit3_5_2_2.text()
        line16_1_2=self.edit4_1_2_2.text()
        line16_2_2=self.edit4_2_2_2.text()
        line16_3_2=self.edit4_3_2_2.text()
        line16_4_2=self.edit4_4_2_2.text()
        line16_5_2=self.edit4_5_2_2.text()
        line17_1_2=self.edit5_1_2_2.text()
        line17_2_2=self.edit5_2_2_2.text()
        line17_3_2=self.edit5_3_2_2.text()
        line17_4_2=self.edit5_4_2_2.text()
        line17_5_2=self.edit5_5_2_2.text()
        line18_1_2=self.edit6_1_2_2.text()
        line18_2_2=self.edit6_2_2_2.text()
        line18_3_2=self.edit6_3_2_2.text()
        line18_4_2=self.edit6_4_2_2.text()
        line18_5_2=self.edit6_5_2_2.text()
        line19_1_2=self.edit7_1_2_2.text()
        line19_2_2=self.edit7_2_2_2.text()
        line19_3_2=self.edit7_3_2_2.text()
        line19_4_2=self.edit7_4_2_2.text()
        line19_5_2=self.edit7_5_2_2.text()
        line20_1_2=self.edit8_1_2_2.text()
        line20_2_2=self.edit8_2_2_2.text()
        line20_3_2=self.edit8_3_2_2.text()
        line20_4_2=self.edit8_4_2_2.text()
        line20_5_2=self.edit8_5_2_2.text()
        line21_1_2=self.edit9_1_2_2.text()
        line21_2_2=self.edit9_2_2_2.text()
        line21_3_2=self.edit9_3_2_2.text()
        line21_4_2=self.edit9_4_2_2.text()
        line21_5_2=self.edit9_5_2_2.text()
        line22_1_2=self.edit10_1_2_2.text()
        line22_2_2=self.edit10_2_2_2.text()
        line22_3_2=self.edit10_3_2_2.text()
        line22_4_2=self.edit10_4_2_2.text()
        line22_5_2=self.edit10_5_2_2.text()
        line23_1_2=self.edit11_1_2_2.text()
        line23_2_2=self.edit11_2_2_2.text()
        line23_3_2=self.edit11_3_2_2.text()
        line23_4_2=self.edit11_4_2_2.text()
        line23_5_2=self.edit11_5_2_2.text()
        line24_1_2=self.edit12_1_2_2.text()
        line24_2_2=self.edit12_2_2_2.text()
        line24_3_2=self.edit12_3_2_2.text()
        line24_4_2=self.edit12_4_2_2.text()
        line24_5_2=self.edit12_5_2_2.text()


        tickers1 = [ticker1_1_1,ticker1_2_1,ticker1_3_1,ticker1_4_1,ticker1_5_1]
        tickers2 = [ticker2_1_1,ticker2_2_1,ticker2_3_1,ticker2_4_1,ticker2_5_1]
        tickers3 = [ticker3_1_1,ticker3_2_1,ticker3_3_1,ticker3_4_1,ticker3_5_1]
        tickers4 = [ticker4_1_1,ticker4_2_1,ticker4_3_1,ticker4_4_1,ticker4_5_1]
        tickers5 = [ticker5_1_1,ticker5_2_1,ticker5_3_1,ticker5_4_1,ticker5_5_1]
        tickers6 = [ticker6_1_1,ticker6_2_1,ticker6_3_1,ticker6_4_1,ticker6_5_1]
        tickers7 = [ticker7_1_1,ticker7_2_1,ticker7_3_1,ticker7_4_1,ticker7_5_1]
        tickers8 = [ticker8_1_1,ticker8_2_1,ticker8_3_1,ticker8_4_1,ticker8_5_1]
        tickers9 = [ticker9_1_1,ticker9_2_1,ticker9_3_1,ticker9_4_1,ticker9_5_1]
        tickers10 = [ticker10_1_1,ticker10_2_1,ticker10_3_1,ticker10_4_1,ticker10_5_1]
        tickers11 = [ticker11_1_1,ticker11_2_1,ticker11_3_1,ticker11_4_1,ticker11_5_1]
        tickers12 = [ticker12_1_1,ticker12_2_1,ticker12_3_1,ticker12_4_1,ticker12_5_1]

        tickers13 = [ticker13_1_1,ticker13_2_1,ticker13_3_1,ticker13_4_1,ticker13_5_1]
        tickers14 = [ticker14_1_1,ticker14_2_1,ticker14_3_1,ticker14_4_1,ticker14_5_1]
        tickers15 = [ticker15_1_1,ticker15_2_1,ticker15_3_1,ticker15_4_1,ticker15_5_1]
        tickers16 = [ticker16_1_1,ticker16_2_1,ticker16_3_1,ticker16_4_1,ticker16_5_1]
        tickers17 = [ticker17_1_1,ticker17_2_1,ticker17_3_1,ticker17_4_1,ticker17_5_1]
        tickers18 = [ticker18_1_1,ticker18_2_1,ticker18_3_1,ticker18_4_1,ticker18_5_1]
        tickers19 = [ticker19_1_1,ticker19_2_1,ticker19_3_1,ticker19_4_1,ticker19_5_1]
        tickers20 = [ticker20_1_1,ticker20_2_1,ticker20_3_1,ticker20_4_1,ticker20_5_1]
        tickers21 = [ticker21_1_1,ticker21_2_1,ticker21_3_1,ticker21_4_1,ticker21_5_1]
        tickers22 = [ticker22_1_1,ticker22_2_1,ticker22_3_1,ticker22_4_1,ticker22_5_1]
        tickers23 = [ticker23_1_1,ticker23_2_1,ticker23_3_1,ticker23_4_1,ticker23_5_1]
        tickers24 = [ticker24_1_1,ticker24_2_1,ticker24_3_1,ticker24_4_1,ticker24_5_1]

        lines1 = [line1_1_2,line1_2_2,line1_3_2,line1_4_2,line1_5_2]
        lines2 = [line2_1_2,line2_2_2,line2_3_2,line2_4_2,line2_5_2]
        lines3 = [line3_1_2,line3_2_2,line3_3_2,line3_4_2,line3_5_2]
        lines4 = [line4_1_2,line4_2_2,line4_3_2,line4_4_2,line4_5_2]
        lines5 = [line5_1_2,line5_2_2,line5_3_2,line5_4_2,line5_5_2]
        lines6 = [line6_1_2,line6_2_2,line6_3_2,line6_4_2,line6_5_2]
        lines7 = [line7_1_2,line7_2_2,line7_3_2,line7_4_2,line7_5_2]
        lines8 = [line8_1_2,line8_2_2,line8_3_2,line8_4_2,line8_5_2]
        lines9 = [line9_1_2,line9_2_2,line9_3_2,line9_4_2,line9_5_2]
        lines10 = [line10_1_2,line10_2_2,line10_3_2,line10_4_2,line10_5_2]
        lines11 = [line11_1_2,line11_2_2,line11_3_2,line11_4_2,line11_5_2]
        lines12 = [line12_1_2,line12_2_2,line12_3_2,line12_4_2,line12_5_2]

        lines13 = [line13_1_2,line13_2_2,line13_3_2,line13_4_2,line13_5_2]
        lines14 = [line14_1_2,line14_2_2,line14_3_2,line14_4_2,line14_5_2]
        lines15 = [line15_1_2,line15_2_2,line15_3_2,line15_4_2,line15_5_2]
        lines16 = [line16_1_2,line16_2_2,line16_3_2,line16_4_2,line16_5_2]
        lines17 = [line17_1_2,line17_2_2,line17_3_2,line17_4_2,line17_5_2]
        lines18 = [line18_1_2,line18_2_2,line18_3_2,line18_4_2,line18_5_2]
        lines19 = [line19_1_2,line19_2_2,line19_3_2,line19_4_2,line19_5_2]
        lines20 = [line20_1_2,line20_2_2,line20_3_2,line20_4_2,line20_5_2]
        lines21 = [line21_1_2,line21_2_2,line21_3_2,line21_4_2,line21_5_2]
        lines22 = [line22_1_2,line22_2_2,line22_3_2,line22_4_2,line22_5_2]
        lines23 = [line23_1_2,line23_2_2,line23_3_2,line23_4_2,line23_5_2]
        lines24 = [line24_1_2,line24_2_2,line24_3_2,line24_4_2,line24_5_2]

        ticker_group = [tickers1,tickers2,tickers3,tickers4,tickers5,tickers6,tickers7,tickers8,tickers9,tickers10,tickers11,tickers12,
                        tickers13,tickers14,tickers15,tickers16,tickers17,tickers18,tickers19,tickers20,tickers21,tickers22,tickers23,tickers24]
        line_group = [lines1,lines2,lines3,lines4,lines5,lines6,lines7,lines8,lines9,lines10,lines11,lines12,
                      lines13,lines14,lines15,lines16,lines17,lines18,lines19,lines20,lines21,lines22,lines23,lines24]
        # print(ticker_group)
        # print(line_group)
        return ticker_group,line_group,duration_s,duration_e
    def db_list(self):
        db_file = "D:/db_files/data.db"
        KRX_file = 'D:/db_files/KRX.db'
        US_file = 'D:/db_files/US.db'
        db_files = [db_file,KRX_file,US_file]
        db_list = []
        KRX_list = []
        US_list = []
        table_list = []
        for i in db_files:
            # print(i,end='')
            con = sqlite3.connect(i)
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_list = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
            if not table_list:
                print('* DB 테이블이 비어있음 - 확인 필요 *')
                return table_list
            elif i == db_file:
                db_list = np.concatenate(table_list).tolist()
                # print(db_list)
            elif i == KRX_file:
                KRX_list = np.concatenate(table_list).tolist()
                # print(KRX_list)
            elif i == US_file:
                US_list = np.concatenate(table_list).tolist()
                # print(US_list)
        return db_list,KRX_list,US_list

    def show_chart(self):
        con_db = sqlite3.connect(db_file)
        con_krx = sqlite3.connect(KRX_file)
        con_us = sqlite3.connect(US_file)
        df = pd.DataFrame()
        graph = []
        ticker_group,line_group,duration_s,duration_e = self.get_edit_text()
        db_list,KRX_list,US_list = self.db_list()
        for j,tickers in enumerate(ticker_group):
            for i,ticker in enumerate(tickers):
                if ticker: #리스트 값이 있으면
                    lines = line_group[j]
                    line = lines[i]
                    # print(ticker,end='-')
                    if ticker in db_list:
                        df_db = pd.read_sql(f"SELECT * FROM '{ticker}'", con_db).set_index('index')
                        # print('db',end='-')
                    elif ticker in KRX_list:
                        df_db = pd.read_sql(f"SELECT * FROM '{ticker}'", con_krx).set_index('index')
                        # print('krx',end='-')
                    elif ticker in US_list:
                        df_db = pd.read_sql(f"SELECT * FROM '{ticker}'", con_us).set_index('index')
                        # print('us',end='-')
                    df_db = df_db[df_db.index >= int(duration_s)]
                    df_db = df_db[df_db.index <= int(duration_e)]
                    s = make_indicator.indicator(df_db,line)
                    s.rename(f'{ticker}_{line}', inplace=True)  # 시리즈의 컬럼명 변경
                    # graph.append(f'{ticker}_{line}')
                elif not ticker: #리스트 값이 없으면
                    s = pd.Series()
                    s.rename(f'_{j+1}{i+1}', inplace=True)  # 시리즈의 컬럼명 변경
                df = pd.concat([df, s], axis=1) #시리즈 병합 합치기
        con_db.close()
        con_krx.close()
        con_us.close()
        con = sqlite3.connect(save_file)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # df = df[df.index >= int(duration_s)]
        # df = df[df.index <= int(duration_e)]
        df.to_sql(now, con, if_exists='replace')
        con.close()
        date = f'{duration_s[:4]}/{duration_s[4:6]}/{duration_s[6:8]} ~ {duration_e[:4]}/{duration_e[4:6]}/{duration_e[6:8]}'
        self.chart = Chart(df, date)
        self.chart.setGeometry(0, 30, 3850, 1010)
        self.chart.show()

    def holic_back(self,delay):
        # print(df_back)
        # df_back.to_excel('table.xlsx')
        print(self.df3)
        self.df3['날짜'] = self.df3.매수시간.astype(str).str[4:8] ##index에서 str짤라가지고 date컬럼 생성
        groups = self.df3.groupby('날짜')  # 날짜별 그룹 만들기
        df_back2 = pd.DataFrame()
        days = list(groups.size().index)
        for day in days:  # 날짜별로접근
            df_mt_date = self.df3[self.df3.날짜 == day]  # 날짜 기준으로 돌아가며 df불러옴
            df_mt_date = df_mt_date.drop_duplicates(['종목코드'])
            df_back2 = pd.concat([df_back2,df_mt_date])
        for i in range(len(df_back2.index)):
            # if df_back2.iloc[i, 3] < 0: #당일수익이 0보다 작은 종목만 표시
                if self.holic_btn2.isChecked() == True:
                    stock_code = df_back2.iloc[i, 0]
                    date = df_back2.iloc[i, -1]
                    stock_name = make_stock_name(stock_code)
                    df = get_data(stock_code, date, start, end, )
                    df = df_add(df,self.edit1_t,self.edit6_t)
                    df = df_backtest(stock_code, df, self.df3)
                    # View_Chart = self.select_chart()
                    self.holic_show_back = Chart(df, stock_name, stock_code, date, self.edit2_t, self.edit3_t, self.edit4_t, self.edit5_t,self.edit7_t)
                    self.holic_show_back.setGeometry(0, 30, 3850, 1010)
                    self.holic_show_back.show()
                    QTest.qWait(delay)
                    self.holic_show_back.close()
                elif self.holic_btn2.isChecked() == False:
                    print(self.holic_btn2.isChecked())
                    self.holic_show_back.close()
                    break
    def holic_vc(self,delay):
        self.df5['날짜'] = self.df5.매수시간.astype(str).str[4:8] ##index에서 str짤라가지고 date컬럼 생성
        groups = self.df5.groupby('날짜')  # 날짜별 그룹 만들기
        df_back2 = pd.DataFrame()
        days = list(groups.size().index)
        for day in days:  # 날짜별로접근
            df_mt_date = self.df5[self.df5.날짜 == day]  # 날짜 기준으로 돌아가며 df불러옴
            df_mt_date = df_mt_date.drop_duplicates(['종목코드']) #중복된 종목코드 삭제
            df_back2 = pd.concat([df_back2,df_mt_date])
        for i in range(len(df_back2.index)):
            # if df_back2.loc[index, '당일수익'] < 0: #당일수익이 0보다 작은 종목만 표시
                if self.holic_btn3.isChecked() == True:
                    stock_code = df_back2.iloc[i,0]
                    date = df_back2.iloc[i,-1]
                    stock_name = make_stock_name(stock_code)
                    df = get_data(stock_code, date, start, end, )
                    df = df_add(df,self.edit1_t,self.edit6_t)
                    df = df_backtest(stock_code, df, self.df5)
                    # View_Chart = self.select_chart()
                    self.holic_show_back = Chart(df, stock_name, stock_code, date, self.edit2_t, self.edit3_t, self.edit4_t, self.edit5_t,self.edit7_t)
                    self.holic_show_back.setGeometry(0, 30, 3850, 1010)
                    self.holic_show_back.show()
                    QTest.qWait(delay)
                    self.holic_show_back.close()
                elif self.holic_btn3.isChecked() == False:
                    # print(self.holic_btn3.isChecked())
                    self.holic_show_back.close()
                    break

    def init_QLineEdit(self):
        self.lbl_chart1 = QLabel('chart 1')
        self.lbl_chart2 = QLabel('chart 2')
        self.lbl_chart3 = QLabel('chart 3')
        self.lbl_chart4 = QLabel('chart 4')
        self.lbl_chart5 = QLabel('chart 5')
        self.lbl_chart6 = QLabel('chart 6')
        self.lbl_chart7 = QLabel('chart 7')
        self.lbl_chart8 = QLabel('chart 8')
        self.lbl_chart9 = QLabel('chart 9')
        self.lbl_chart10 = QLabel('chart 10')
        self.lbl_chart11 = QLabel('chart 11')
        self.lbl_chart12 = QLabel('chart 12')
        self.edit1_1_1 = QLineEdit(self)
        self.edit1_1_2 = QLineEdit(self)
        self.edit1_2_1 = QLineEdit(self)
        self.edit1_2_2 = QLineEdit(self)
        self.edit1_3_1 = QLineEdit(self)
        self.edit1_3_2 = QLineEdit(self)
        self.edit1_4_1 = QLineEdit(self)
        self.edit1_4_2 = QLineEdit(self)
        self.edit1_5_1 = QLineEdit(self)
        self.edit1_5_2 = QLineEdit(self)
        self.edit2_1_1 = QLineEdit(self)
        self.edit2_1_2 = QLineEdit(self)
        self.edit2_2_1 = QLineEdit(self)
        self.edit2_2_2 = QLineEdit(self)
        self.edit2_3_1 = QLineEdit(self)
        self.edit2_3_2 = QLineEdit(self)
        self.edit2_4_1 = QLineEdit(self)
        self.edit2_4_2 = QLineEdit(self)
        self.edit2_5_1 = QLineEdit(self)
        self.edit2_5_2 = QLineEdit(self)
        self.edit3_1_1 = QLineEdit(self)
        self.edit3_1_2 = QLineEdit(self)
        self.edit3_2_1 = QLineEdit(self)
        self.edit3_2_2 = QLineEdit(self)
        self.edit3_3_1 = QLineEdit(self)
        self.edit3_3_2 = QLineEdit(self)
        self.edit3_4_1 = QLineEdit(self)
        self.edit3_4_2 = QLineEdit(self)
        self.edit3_5_1 = QLineEdit(self)
        self.edit3_5_2 = QLineEdit(self)
        self.edit4_1_1 = QLineEdit(self)
        self.edit4_1_2 = QLineEdit(self)
        self.edit4_2_1 = QLineEdit(self)
        self.edit4_2_2 = QLineEdit(self)
        self.edit4_3_1 = QLineEdit(self)
        self.edit4_3_2 = QLineEdit(self)
        self.edit4_4_1 = QLineEdit(self)
        self.edit4_4_2 = QLineEdit(self)
        self.edit4_5_1 = QLineEdit(self)
        self.edit4_5_2 = QLineEdit(self)
        self.edit5_1_1 = QLineEdit(self)
        self.edit5_1_2 = QLineEdit(self)
        self.edit5_2_1 = QLineEdit(self)
        self.edit5_2_2 = QLineEdit(self)
        self.edit5_3_1 = QLineEdit(self)
        self.edit5_3_2 = QLineEdit(self)
        self.edit5_4_1 = QLineEdit(self)
        self.edit5_4_2 = QLineEdit(self)
        self.edit5_5_1 = QLineEdit(self)
        self.edit5_5_2 = QLineEdit(self)
        self.edit6_1_1 = QLineEdit(self)
        self.edit6_1_2 = QLineEdit(self)
        self.edit6_2_1 = QLineEdit(self)
        self.edit6_2_2 = QLineEdit(self)
        self.edit6_3_1 = QLineEdit(self)
        self.edit6_3_2 = QLineEdit(self)
        self.edit6_4_1 = QLineEdit(self)
        self.edit6_4_2 = QLineEdit(self)
        self.edit6_5_1 = QLineEdit(self)
        self.edit6_5_2 = QLineEdit(self)
        self.edit7_1_1 = QLineEdit(self)
        self.edit7_1_2 = QLineEdit(self)
        self.edit7_2_1 = QLineEdit(self)
        self.edit7_2_2 = QLineEdit(self)
        self.edit7_3_1 = QLineEdit(self)
        self.edit7_3_2 = QLineEdit(self)
        self.edit7_4_1 = QLineEdit(self)
        self.edit7_4_2 = QLineEdit(self)
        self.edit7_5_1 = QLineEdit(self)
        self.edit7_5_2 = QLineEdit(self)
        self.edit8_1_1 = QLineEdit(self)
        self.edit8_1_2 = QLineEdit(self)
        self.edit8_2_1 = QLineEdit(self)
        self.edit8_2_2 = QLineEdit(self)
        self.edit8_3_1 = QLineEdit(self)
        self.edit8_3_2 = QLineEdit(self)
        self.edit8_4_1 = QLineEdit(self)
        self.edit8_4_2 = QLineEdit(self)
        self.edit8_5_1 = QLineEdit(self)
        self.edit8_5_2 = QLineEdit(self)
        self.edit9_1_1 = QLineEdit(self)
        self.edit9_1_2 = QLineEdit(self)
        self.edit9_2_1 = QLineEdit(self)
        self.edit9_2_2 = QLineEdit(self)
        self.edit9_3_1 = QLineEdit(self)
        self.edit9_3_2 = QLineEdit(self)
        self.edit9_4_1 = QLineEdit(self)
        self.edit9_4_2 = QLineEdit(self)
        self.edit9_5_1 = QLineEdit(self)
        self.edit9_5_2 = QLineEdit(self)
        self.edit10_1_1 = QLineEdit(self)
        self.edit10_1_2 = QLineEdit(self)
        self.edit10_2_1 = QLineEdit(self)
        self.edit10_2_2 = QLineEdit(self)
        self.edit10_3_1 = QLineEdit(self)
        self.edit10_3_2 = QLineEdit(self)
        self.edit10_4_1 = QLineEdit(self)
        self.edit10_4_2 = QLineEdit(self)
        self.edit10_5_1 = QLineEdit(self)
        self.edit10_5_2 = QLineEdit(self)
        self.edit11_1_1 = QLineEdit(self)
        self.edit11_1_2 = QLineEdit(self)
        self.edit11_2_1 = QLineEdit(self)
        self.edit11_2_2 = QLineEdit(self)
        self.edit11_3_1 = QLineEdit(self)
        self.edit11_3_2 = QLineEdit(self)
        self.edit11_4_1 = QLineEdit(self)
        self.edit11_4_2 = QLineEdit(self)
        self.edit11_5_1 = QLineEdit(self)
        self.edit11_5_2 = QLineEdit(self)
        self.edit12_1_1 = QLineEdit(self)
        self.edit12_1_2 = QLineEdit(self)
        self.edit12_2_1 = QLineEdit(self)
        self.edit12_2_2 = QLineEdit(self)
        self.edit12_3_1 = QLineEdit(self)
        self.edit12_3_2 = QLineEdit(self)
        self.edit12_4_1 = QLineEdit(self)
        self.edit12_4_2 = QLineEdit(self)
        self.edit12_5_1 = QLineEdit(self)
        self.edit12_5_2 = QLineEdit(self)

        self.lbl_chart1_2 = QLabel('chart 1')
        self.lbl_chart2_2 = QLabel('chart 2')
        self.lbl_chart3_2 = QLabel('chart 3')
        self.lbl_chart4_2 = QLabel('chart 4')
        self.lbl_chart5_2 = QLabel('chart 5')
        self.lbl_chart6_2 = QLabel('chart 6')
        self.lbl_chart7_2 = QLabel('chart 7')
        self.lbl_chart8_2 = QLabel('chart 8')
        self.lbl_chart9_2 = QLabel('chart 9')
        self.lbl_chart10_2 = QLabel('chart 10')
        self.lbl_chart11_2 = QLabel('chart 11')
        self.lbl_chart12_2 = QLabel('chart 12')
        self.edit1_1_1_2 = QLineEdit(self)
        self.edit1_1_2_2 = QLineEdit(self)
        self.edit1_2_1_2 = QLineEdit(self)
        self.edit1_2_2_2 = QLineEdit(self)
        self.edit1_3_1_2 = QLineEdit(self)
        self.edit1_3_2_2 = QLineEdit(self)
        self.edit1_4_1_2 = QLineEdit(self)
        self.edit1_4_2_2 = QLineEdit(self)
        self.edit1_5_1_2 = QLineEdit(self)
        self.edit1_5_2_2 = QLineEdit(self)
        self.edit2_1_1_2 = QLineEdit(self)
        self.edit2_1_2_2 = QLineEdit(self)
        self.edit2_2_1_2 = QLineEdit(self)
        self.edit2_2_2_2 = QLineEdit(self)
        self.edit2_3_1_2 = QLineEdit(self)
        self.edit2_3_2_2 = QLineEdit(self)
        self.edit2_4_1_2 = QLineEdit(self)
        self.edit2_4_2_2 = QLineEdit(self)
        self.edit2_5_1_2 = QLineEdit(self)
        self.edit2_5_2_2 = QLineEdit(self)
        self.edit3_1_1_2 = QLineEdit(self)
        self.edit3_1_2_2 = QLineEdit(self)
        self.edit3_2_1_2 = QLineEdit(self)
        self.edit3_2_2_2 = QLineEdit(self)
        self.edit3_3_1_2 = QLineEdit(self)
        self.edit3_3_2_2 = QLineEdit(self)
        self.edit3_4_1_2 = QLineEdit(self)
        self.edit3_4_2_2 = QLineEdit(self)
        self.edit3_5_1_2 = QLineEdit(self)
        self.edit3_5_2_2 = QLineEdit(self)
        self.edit4_1_1_2 = QLineEdit(self)
        self.edit4_1_2_2 = QLineEdit(self)
        self.edit4_2_1_2 = QLineEdit(self)
        self.edit4_2_2_2 = QLineEdit(self)
        self.edit4_3_1_2 = QLineEdit(self)
        self.edit4_3_2_2 = QLineEdit(self)
        self.edit4_4_1_2 = QLineEdit(self)
        self.edit4_4_2_2 = QLineEdit(self)
        self.edit4_5_1_2 = QLineEdit(self)
        self.edit4_5_2_2 = QLineEdit(self)
        self.edit5_1_1_2 = QLineEdit(self)
        self.edit5_1_2_2 = QLineEdit(self)
        self.edit5_2_1_2 = QLineEdit(self)
        self.edit5_2_2_2 = QLineEdit(self)
        self.edit5_3_1_2 = QLineEdit(self)
        self.edit5_3_2_2 = QLineEdit(self)
        self.edit5_4_1_2 = QLineEdit(self)
        self.edit5_4_2_2 = QLineEdit(self)
        self.edit5_5_1_2 = QLineEdit(self)
        self.edit5_5_2_2 = QLineEdit(self)
        self.edit6_1_1_2 = QLineEdit(self)
        self.edit6_1_2_2 = QLineEdit(self)
        self.edit6_2_1_2 = QLineEdit(self)
        self.edit6_2_2_2 = QLineEdit(self)
        self.edit6_3_1_2 = QLineEdit(self)
        self.edit6_3_2_2 = QLineEdit(self)
        self.edit6_4_1_2 = QLineEdit(self)
        self.edit6_4_2_2 = QLineEdit(self)
        self.edit6_5_1_2 = QLineEdit(self)
        self.edit6_5_2_2 = QLineEdit(self)
        self.edit7_1_1_2 = QLineEdit(self)
        self.edit7_1_2_2 = QLineEdit(self)
        self.edit7_2_1_2 = QLineEdit(self)
        self.edit7_2_2_2 = QLineEdit(self)
        self.edit7_3_1_2 = QLineEdit(self)
        self.edit7_3_2_2 = QLineEdit(self)
        self.edit7_4_1_2 = QLineEdit(self)
        self.edit7_4_2_2 = QLineEdit(self)
        self.edit7_5_1_2 = QLineEdit(self)
        self.edit7_5_2_2 = QLineEdit(self)
        self.edit8_1_1_2 = QLineEdit(self)
        self.edit8_1_2_2 = QLineEdit(self)
        self.edit8_2_1_2 = QLineEdit(self)
        self.edit8_2_2_2 = QLineEdit(self)
        self.edit8_3_1_2 = QLineEdit(self)
        self.edit8_3_2_2 = QLineEdit(self)
        self.edit8_4_1_2 = QLineEdit(self)
        self.edit8_4_2_2 = QLineEdit(self)
        self.edit8_5_1_2 = QLineEdit(self)
        self.edit8_5_2_2 = QLineEdit(self)
        self.edit9_1_1_2 = QLineEdit(self)
        self.edit9_1_2_2 = QLineEdit(self)
        self.edit9_2_1_2 = QLineEdit(self)
        self.edit9_2_2_2 = QLineEdit(self)
        self.edit9_3_1_2 = QLineEdit(self)
        self.edit9_3_2_2 = QLineEdit(self)
        self.edit9_4_1_2 = QLineEdit(self)
        self.edit9_4_2_2 = QLineEdit(self)
        self.edit9_5_1_2 = QLineEdit(self)
        self.edit9_5_2_2 = QLineEdit(self)
        self.edit10_1_1_2 = QLineEdit(self)
        self.edit10_1_2_2 = QLineEdit(self)
        self.edit10_2_1_2 = QLineEdit(self)
        self.edit10_2_2_2 = QLineEdit(self)
        self.edit10_3_1_2 = QLineEdit(self)
        self.edit10_3_2_2 = QLineEdit(self)
        self.edit10_4_1_2 = QLineEdit(self)
        self.edit10_4_2_2 = QLineEdit(self)
        self.edit10_5_1_2 = QLineEdit(self)
        self.edit10_5_2_2 = QLineEdit(self)
        self.edit11_1_1_2 = QLineEdit(self)
        self.edit11_1_2_2 = QLineEdit(self)
        self.edit11_2_1_2 = QLineEdit(self)
        self.edit11_2_2_2 = QLineEdit(self)
        self.edit11_3_1_2 = QLineEdit(self)
        self.edit11_3_2_2 = QLineEdit(self)
        self.edit11_4_1_2 = QLineEdit(self)
        self.edit11_4_2_2 = QLineEdit(self)
        self.edit11_5_1_2 = QLineEdit(self)
        self.edit11_5_2_2 = QLineEdit(self)
        self.edit12_1_1_2 = QLineEdit(self)
        self.edit12_1_2_2 = QLineEdit(self)
        self.edit12_2_1_2 = QLineEdit(self)
        self.edit12_2_2_2 = QLineEdit(self)
        self.edit12_3_1_2 = QLineEdit(self)
        self.edit12_3_2_2 = QLineEdit(self)
        self.edit12_4_1_2 = QLineEdit(self)
        self.edit12_4_2_2 = QLineEdit(self)
        self.edit12_5_1_2 = QLineEdit(self)
        self.edit12_5_2_2 = QLineEdit(self)
    def init_grid(self):
        self.grid_chart1.addWidget(self.lbl_chart1, 0, 0)
        self.grid_chart1.addWidget(self.edit1_1_1, 1, 0)
        self.grid_chart1.addWidget(self.edit1_1_2, 1, 1)
        self.grid_chart1.addWidget(self.edit1_2_1, 2, 0)
        self.grid_chart1.addWidget(self.edit1_2_2, 2, 1)
        self.grid_chart1.addWidget(self.edit1_3_1, 3, 0)
        self.grid_chart1.addWidget(self.edit1_3_2, 3, 1)
        self.grid_chart1.addWidget(self.edit1_4_1, 4, 0)
        self.grid_chart1.addWidget(self.edit1_4_2, 4, 1)
        self.grid_chart1.addWidget(self.edit1_5_1, 5, 0)
        self.grid_chart1.addWidget(self.edit1_5_2, 5, 1)
        self.grid_chart1.addWidget(self.lbl_chart2, 6, 0)
        self.grid_chart1.addWidget(self.edit2_1_1, 7, 0)
        self.grid_chart1.addWidget(self.edit2_1_2, 7, 1)
        self.grid_chart1.addWidget(self.edit2_2_1, 8, 0)
        self.grid_chart1.addWidget(self.edit2_2_2, 8, 1)
        self.grid_chart1.addWidget(self.edit2_3_1, 9, 0)
        self.grid_chart1.addWidget(self.edit2_3_2, 9, 1)
        self.grid_chart1.addWidget(self.edit2_4_1, 10, 0)
        self.grid_chart1.addWidget(self.edit2_4_2, 10, 1)
        self.grid_chart1.addWidget(self.edit2_5_1, 11, 0)
        self.grid_chart1.addWidget(self.edit2_5_2, 11, 1)
        self.grid_chart1.addWidget(self.lbl_chart3, 12, 0)
        self.grid_chart1.addWidget(self.edit3_1_1, 13, 0)
        self.grid_chart1.addWidget(self.edit3_1_2, 13, 1)
        self.grid_chart1.addWidget(self.edit3_2_1, 14, 0)
        self.grid_chart1.addWidget(self.edit3_2_2, 14, 1)
        self.grid_chart1.addWidget(self.edit3_3_1, 15, 0)
        self.grid_chart1.addWidget(self.edit3_3_2, 15, 1)
        self.grid_chart1.addWidget(self.edit3_4_1, 16, 0)
        self.grid_chart1.addWidget(self.edit3_4_2, 16, 1)
        self.grid_chart1.addWidget(self.edit3_5_1, 17, 0)
        self.grid_chart1.addWidget(self.edit3_5_2, 17, 1)
        self.grid_chart1.addWidget(self.lbl_chart4, 0, 2)
        self.grid_chart1.addWidget(self.edit4_1_1, 1, 2)
        self.grid_chart1.addWidget(self.edit4_1_2, 1, 3)
        self.grid_chart1.addWidget(self.edit4_2_1, 2, 2)
        self.grid_chart1.addWidget(self.edit4_2_2, 2, 3)
        self.grid_chart1.addWidget(self.edit4_3_1, 3, 2)
        self.grid_chart1.addWidget(self.edit4_3_2, 3, 3)
        self.grid_chart1.addWidget(self.edit4_4_1, 4, 2)
        self.grid_chart1.addWidget(self.edit4_4_2, 4, 3)
        self.grid_chart1.addWidget(self.edit4_5_1, 5, 2)
        self.grid_chart1.addWidget(self.edit4_5_2, 5, 3)
        self.grid_chart1.addWidget(self.lbl_chart5, 6, 2)
        self.grid_chart1.addWidget(self.edit5_1_1, 7, 2)
        self.grid_chart1.addWidget(self.edit5_1_2, 7, 3)
        self.grid_chart1.addWidget(self.edit5_2_1, 8, 2)
        self.grid_chart1.addWidget(self.edit5_2_2, 8, 3)
        self.grid_chart1.addWidget(self.edit5_3_1, 9, 2)
        self.grid_chart1.addWidget(self.edit5_3_2, 9, 3)
        self.grid_chart1.addWidget(self.edit5_4_1, 10, 2)
        self.grid_chart1.addWidget(self.edit5_4_2, 10, 3)
        self.grid_chart1.addWidget(self.edit5_5_1, 11, 2)
        self.grid_chart1.addWidget(self.edit5_5_2, 11, 3)
        self.grid_chart1.addWidget(self.lbl_chart6, 12, 2)
        self.grid_chart1.addWidget(self.edit6_1_1, 13, 2)
        self.grid_chart1.addWidget(self.edit6_1_2, 13, 3)
        self.grid_chart1.addWidget(self.edit6_2_1, 14, 2)
        self.grid_chart1.addWidget(self.edit6_2_2, 14, 3)
        self.grid_chart1.addWidget(self.edit6_3_1, 15, 2)
        self.grid_chart1.addWidget(self.edit6_3_2, 15, 3)
        self.grid_chart1.addWidget(self.edit6_4_1, 16, 2)
        self.grid_chart1.addWidget(self.edit6_4_2, 16, 3)
        self.grid_chart1.addWidget(self.edit6_5_1, 17, 2)
        self.grid_chart1.addWidget(self.edit6_5_2, 17, 3)
        self.grid_chart1.addWidget(self.lbl_chart7, 0, 4)
        self.grid_chart1.addWidget(self.edit7_1_1, 1, 4)
        self.grid_chart1.addWidget(self.edit7_1_2, 1, 5)
        self.grid_chart1.addWidget(self.edit7_2_1, 2, 4)
        self.grid_chart1.addWidget(self.edit7_2_2, 2, 5)
        self.grid_chart1.addWidget(self.edit7_3_1, 3, 4)
        self.grid_chart1.addWidget(self.edit7_3_2, 3, 5)
        self.grid_chart1.addWidget(self.edit7_4_1, 4, 4)
        self.grid_chart1.addWidget(self.edit7_4_2, 4, 5)
        self.grid_chart1.addWidget(self.edit7_5_1, 5, 4)
        self.grid_chart1.addWidget(self.edit7_5_2, 5, 5)
        self.grid_chart1.addWidget(self.lbl_chart8, 6, 4)
        self.grid_chart1.addWidget(self.edit8_1_1, 7, 4)
        self.grid_chart1.addWidget(self.edit8_1_2, 7, 5)
        self.grid_chart1.addWidget(self.edit8_2_1, 8, 4)
        self.grid_chart1.addWidget(self.edit8_2_2, 8, 5)
        self.grid_chart1.addWidget(self.edit8_3_1, 9, 4)
        self.grid_chart1.addWidget(self.edit8_3_2, 9, 5)
        self.grid_chart1.addWidget(self.edit8_4_1, 10, 4)
        self.grid_chart1.addWidget(self.edit8_4_2, 10, 5)
        self.grid_chart1.addWidget(self.edit8_5_1, 11, 4)
        self.grid_chart1.addWidget(self.edit8_5_2, 11, 5)
        self.grid_chart1.addWidget(self.lbl_chart9, 12, 4)
        self.grid_chart1.addWidget(self.edit9_1_1, 13, 4)
        self.grid_chart1.addWidget(self.edit9_1_2, 13, 5)
        self.grid_chart1.addWidget(self.edit9_2_1, 14, 4)
        self.grid_chart1.addWidget(self.edit9_2_2, 14, 5)
        self.grid_chart1.addWidget(self.edit9_3_1, 15, 4)
        self.grid_chart1.addWidget(self.edit9_3_2, 15, 5)
        self.grid_chart1.addWidget(self.edit9_4_1, 16, 4)
        self.grid_chart1.addWidget(self.edit9_4_2, 16, 5)
        self.grid_chart1.addWidget(self.edit9_5_1, 17, 4)
        self.grid_chart1.addWidget(self.edit9_5_2, 17, 5)
        self.grid_chart1.addWidget(self.lbl_chart10, 0, 6)
        self.grid_chart1.addWidget(self.edit10_1_1, 1, 6)
        self.grid_chart1.addWidget(self.edit10_1_2, 1, 7)
        self.grid_chart1.addWidget(self.edit10_2_1, 2, 6)
        self.grid_chart1.addWidget(self.edit10_2_2, 2, 7)
        self.grid_chart1.addWidget(self.edit10_3_1, 3, 6)
        self.grid_chart1.addWidget(self.edit10_3_2, 3, 7)
        self.grid_chart1.addWidget(self.edit10_4_1, 4, 6)
        self.grid_chart1.addWidget(self.edit10_4_2, 4, 7)
        self.grid_chart1.addWidget(self.edit10_5_1, 5, 6)
        self.grid_chart1.addWidget(self.edit10_5_2, 5, 7)
        self.grid_chart1.addWidget(self.lbl_chart11, 6, 6)
        self.grid_chart1.addWidget(self.edit11_1_1, 7, 6)
        self.grid_chart1.addWidget(self.edit11_1_2, 7, 7)
        self.grid_chart1.addWidget(self.edit11_2_1, 8, 6)
        self.grid_chart1.addWidget(self.edit11_2_2, 8, 7)
        self.grid_chart1.addWidget(self.edit11_3_1, 9, 6)
        self.grid_chart1.addWidget(self.edit11_3_2, 9, 7)
        self.grid_chart1.addWidget(self.edit11_4_1, 10, 6)
        self.grid_chart1.addWidget(self.edit11_4_2, 10, 7)
        self.grid_chart1.addWidget(self.edit11_5_1, 11, 6)
        self.grid_chart1.addWidget(self.edit11_5_2, 11, 7)
        self.grid_chart1.addWidget(self.lbl_chart12, 12, 6)
        self.grid_chart1.addWidget(self.edit12_1_1, 13, 6)
        self.grid_chart1.addWidget(self.edit12_1_2, 13, 7)
        self.grid_chart1.addWidget(self.edit12_2_1, 14, 6)
        self.grid_chart1.addWidget(self.edit12_2_2, 14, 7)
        self.grid_chart1.addWidget(self.edit12_3_1, 15, 6)
        self.grid_chart1.addWidget(self.edit12_3_2, 15, 7)
        self.grid_chart1.addWidget(self.edit12_4_1, 16, 6)
        self.grid_chart1.addWidget(self.edit12_4_2, 16, 7)
        self.grid_chart1.addWidget(self.edit12_5_1, 17, 6)
        self.grid_chart1.addWidget(self.edit12_5_2, 17, 7)

        self.grid_chart2.addWidget(self.lbl_chart1_2, 0, 0)
        self.grid_chart2.addWidget(self.edit1_1_1_2, 1, 0)
        self.grid_chart2.addWidget(self.edit1_1_2_2, 1, 1)
        self.grid_chart2.addWidget(self.edit1_2_1_2, 2, 0)
        self.grid_chart2.addWidget(self.edit1_2_2_2, 2, 1)
        self.grid_chart2.addWidget(self.edit1_3_1_2, 3, 0)
        self.grid_chart2.addWidget(self.edit1_3_2_2, 3, 1)
        self.grid_chart2.addWidget(self.edit1_4_1_2, 4, 0)
        self.grid_chart2.addWidget(self.edit1_4_2_2, 4, 1)
        self.grid_chart2.addWidget(self.edit1_5_1_2, 5, 0)
        self.grid_chart2.addWidget(self.edit1_5_2_2, 5, 1)
        self.grid_chart2.addWidget(self.lbl_chart2_2, 6, 0)
        self.grid_chart2.addWidget(self.edit2_1_1_2, 7, 0)
        self.grid_chart2.addWidget(self.edit2_1_2_2, 7, 1)
        self.grid_chart2.addWidget(self.edit2_2_1_2, 8, 0)
        self.grid_chart2.addWidget(self.edit2_2_2_2, 8, 1)
        self.grid_chart2.addWidget(self.edit2_3_1_2, 9, 0)
        self.grid_chart2.addWidget(self.edit2_3_2_2, 9, 1)
        self.grid_chart2.addWidget(self.edit2_4_1_2, 10, 0)
        self.grid_chart2.addWidget(self.edit2_4_2_2, 10, 1)
        self.grid_chart2.addWidget(self.edit2_5_1_2, 11, 0)
        self.grid_chart2.addWidget(self.edit2_5_2_2, 11, 1)
        self.grid_chart2.addWidget(self.lbl_chart3_2, 12, 0)
        self.grid_chart2.addWidget(self.edit3_1_1_2, 13, 0)
        self.grid_chart2.addWidget(self.edit3_1_2_2, 13, 1)
        self.grid_chart2.addWidget(self.edit3_2_1_2, 14, 0)
        self.grid_chart2.addWidget(self.edit3_2_2_2, 14, 1)
        self.grid_chart2.addWidget(self.edit3_3_1_2, 15, 0)
        self.grid_chart2.addWidget(self.edit3_3_2_2, 15, 1)
        self.grid_chart2.addWidget(self.edit3_4_1_2, 16, 0)
        self.grid_chart2.addWidget(self.edit3_4_2_2, 16, 1)
        self.grid_chart2.addWidget(self.edit3_5_1_2, 17, 0)
        self.grid_chart2.addWidget(self.edit3_5_2_2, 17, 1)
        self.grid_chart2.addWidget(self.lbl_chart4_2, 0, 2)
        self.grid_chart2.addWidget(self.edit4_1_1_2, 1, 2)
        self.grid_chart2.addWidget(self.edit4_1_2_2, 1, 3)
        self.grid_chart2.addWidget(self.edit4_2_1_2, 2, 2)
        self.grid_chart2.addWidget(self.edit4_2_2_2, 2, 3)
        self.grid_chart2.addWidget(self.edit4_3_1_2, 3, 2)
        self.grid_chart2.addWidget(self.edit4_3_2_2, 3, 3)
        self.grid_chart2.addWidget(self.edit4_4_1_2, 4, 2)
        self.grid_chart2.addWidget(self.edit4_4_2_2, 4, 3)
        self.grid_chart2.addWidget(self.edit4_5_1_2, 5, 2)
        self.grid_chart2.addWidget(self.edit4_5_2_2, 5, 3)
        self.grid_chart2.addWidget(self.lbl_chart5_2, 6, 2)
        self.grid_chart2.addWidget(self.edit5_1_1_2, 7, 2)
        self.grid_chart2.addWidget(self.edit5_1_2_2, 7, 3)
        self.grid_chart2.addWidget(self.edit5_2_1_2, 8, 2)
        self.grid_chart2.addWidget(self.edit5_2_2_2, 8, 3)
        self.grid_chart2.addWidget(self.edit5_3_1_2, 9, 2)
        self.grid_chart2.addWidget(self.edit5_3_2_2, 9, 3)
        self.grid_chart2.addWidget(self.edit5_4_1_2, 10, 2)
        self.grid_chart2.addWidget(self.edit5_4_2_2, 10, 3)
        self.grid_chart2.addWidget(self.edit5_5_1_2, 11, 2)
        self.grid_chart2.addWidget(self.edit5_5_2_2, 11, 3)
        self.grid_chart2.addWidget(self.lbl_chart6_2, 12, 2)
        self.grid_chart2.addWidget(self.edit6_1_1_2, 13, 2)
        self.grid_chart2.addWidget(self.edit6_1_2_2, 13, 3)
        self.grid_chart2.addWidget(self.edit6_2_1_2, 14, 2)
        self.grid_chart2.addWidget(self.edit6_2_2_2, 14, 3)
        self.grid_chart2.addWidget(self.edit6_3_1_2, 15, 2)
        self.grid_chart2.addWidget(self.edit6_3_2_2, 15, 3)
        self.grid_chart2.addWidget(self.edit6_4_1_2, 16, 2)
        self.grid_chart2.addWidget(self.edit6_4_2_2, 16, 3)
        self.grid_chart2.addWidget(self.edit6_5_1_2, 17, 2)
        self.grid_chart2.addWidget(self.edit6_5_2_2, 17, 3)
        self.grid_chart2.addWidget(self.lbl_chart7_2, 0, 4)
        self.grid_chart2.addWidget(self.edit7_1_1_2, 1, 4)
        self.grid_chart2.addWidget(self.edit7_1_2_2, 1, 5)
        self.grid_chart2.addWidget(self.edit7_2_1_2, 2, 4)
        self.grid_chart2.addWidget(self.edit7_2_2_2, 2, 5)
        self.grid_chart2.addWidget(self.edit7_3_1_2, 3, 4)
        self.grid_chart2.addWidget(self.edit7_3_2_2, 3, 5)
        self.grid_chart2.addWidget(self.edit7_4_1_2, 4, 4)
        self.grid_chart2.addWidget(self.edit7_4_2_2, 4, 5)
        self.grid_chart2.addWidget(self.edit7_5_1_2, 5, 4)
        self.grid_chart2.addWidget(self.edit7_5_2_2, 5, 5)
        self.grid_chart2.addWidget(self.lbl_chart8_2, 6, 4)
        self.grid_chart2.addWidget(self.edit8_1_1_2, 7, 4)
        self.grid_chart2.addWidget(self.edit8_1_2_2, 7, 5)
        self.grid_chart2.addWidget(self.edit8_2_1_2, 8, 4)
        self.grid_chart2.addWidget(self.edit8_2_2_2, 8, 5)
        self.grid_chart2.addWidget(self.edit8_3_1_2, 9, 4)
        self.grid_chart2.addWidget(self.edit8_3_2_2, 9, 5)
        self.grid_chart2.addWidget(self.edit8_4_1_2, 10, 4)
        self.grid_chart2.addWidget(self.edit8_4_2_2, 10, 5)
        self.grid_chart2.addWidget(self.edit8_5_1_2, 11, 4)
        self.grid_chart2.addWidget(self.edit8_5_2_2, 11, 5)
        self.grid_chart2.addWidget(self.lbl_chart9_2, 12, 4)
        self.grid_chart2.addWidget(self.edit9_1_1_2, 13, 4)
        self.grid_chart2.addWidget(self.edit9_1_2_2, 13, 5)
        self.grid_chart2.addWidget(self.edit9_2_1_2, 14, 4)
        self.grid_chart2.addWidget(self.edit9_2_2_2, 14, 5)
        self.grid_chart2.addWidget(self.edit9_3_1_2, 15, 4)
        self.grid_chart2.addWidget(self.edit9_3_2_2, 15, 5)
        self.grid_chart2.addWidget(self.edit9_4_1_2, 16, 4)
        self.grid_chart2.addWidget(self.edit9_4_2_2, 16, 5)
        self.grid_chart2.addWidget(self.edit9_5_1_2, 17, 4)
        self.grid_chart2.addWidget(self.edit9_5_2_2, 17, 5)
        self.grid_chart2.addWidget(self.lbl_chart10_2, 0, 6)
        self.grid_chart2.addWidget(self.edit10_1_1_2, 1, 6)
        self.grid_chart2.addWidget(self.edit10_1_2_2, 1, 7)
        self.grid_chart2.addWidget(self.edit10_2_1_2, 2, 6)
        self.grid_chart2.addWidget(self.edit10_2_2_2, 2, 7)
        self.grid_chart2.addWidget(self.edit10_3_1_2, 3, 6)
        self.grid_chart2.addWidget(self.edit10_3_2_2, 3, 7)
        self.grid_chart2.addWidget(self.edit10_4_1_2, 4, 6)
        self.grid_chart2.addWidget(self.edit10_4_2_2, 4, 7)
        self.grid_chart2.addWidget(self.edit10_5_1_2, 5, 6)
        self.grid_chart2.addWidget(self.edit10_5_2_2, 5, 7)
        self.grid_chart2.addWidget(self.lbl_chart11_2, 6, 6)
        self.grid_chart2.addWidget(self.edit11_1_1_2, 7, 6)
        self.grid_chart2.addWidget(self.edit11_1_2_2, 7, 7)
        self.grid_chart2.addWidget(self.edit11_2_1_2, 8, 6)
        self.grid_chart2.addWidget(self.edit11_2_2_2, 8, 7)
        self.grid_chart2.addWidget(self.edit11_3_1_2, 9, 6)
        self.grid_chart2.addWidget(self.edit11_3_2_2, 9, 7)
        self.grid_chart2.addWidget(self.edit11_4_1_2, 10, 6)
        self.grid_chart2.addWidget(self.edit11_4_2_2, 10, 7)
        self.grid_chart2.addWidget(self.edit11_5_1_2, 11, 6)
        self.grid_chart2.addWidget(self.edit11_5_2_2, 11, 7)
        self.grid_chart2.addWidget(self.lbl_chart12_2, 12, 6)
        self.grid_chart2.addWidget(self.edit12_1_1_2, 13, 6)
        self.grid_chart2.addWidget(self.edit12_1_2_2, 13, 7)
        self.grid_chart2.addWidget(self.edit12_2_1_2, 14, 6)
        self.grid_chart2.addWidget(self.edit12_2_2_2, 14, 7)
        self.grid_chart2.addWidget(self.edit12_3_1_2, 15, 6)
        self.grid_chart2.addWidget(self.edit12_3_2_2, 15, 7)
        self.grid_chart2.addWidget(self.edit12_4_1_2, 16, 6)
        self.grid_chart2.addWidget(self.edit12_4_2_2, 16, 7)
        self.grid_chart2.addWidget(self.edit12_5_1_2, 17, 6)
        self.grid_chart2.addWidget(self.edit12_5_2_2, 17, 7)
    def import_name(self):
        con = sqlite3.connect(save_file)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
        if not table_list:
            print('* DB 테이블이 비어있음 - 확인 필요 *')
        table_list = np.concatenate(table_list).tolist()
        df = pd.read_sql(f"SELECT * FROM '{table_list[-1]}'", con).set_index('index')
        list_df = df.columns.tolist()
        if len(list_df) <120:
            list_df = ['_' for x in range(120)]
        ticker_list = []
        line_list =[]
        for x in list_df:
            p = x.find('_')
            ticker_list.append(str(x)[:p])
        for x in list_df:
            p = x.find('_')
            val=str(x)[p + 1:]
            if str.isdigit(val): #리스트가 숫자로만 이루어졌으면
                line_list.append('')
            else:
                line_list.append(val)
                # print(str(x)[p+1:])
        # print(ticker_list)
        # print(line_list)
        duration_s = df.index[0].astype(str)
        duration_e = df.index[-1].astype(str)
        self.edit_start_1.setText(duration_s)
        self.edit_end_1.setText(duration_e)
        self.edit1_1_1.setText(ticker_list[0])
        self.edit1_2_1.setText(ticker_list[1])
        self.edit1_3_1.setText(ticker_list[2])
        self.edit1_4_1.setText(ticker_list[3])
        self.edit1_5_1.setText(ticker_list[4])
        self.edit2_1_1.setText(ticker_list[5])
        self.edit2_2_1.setText(ticker_list[6])
        self.edit2_3_1.setText(ticker_list[7])
        self.edit2_4_1.setText(ticker_list[8])
        self.edit2_5_1.setText(ticker_list[9])
        self.edit3_1_1.setText(ticker_list[10])
        self.edit3_2_1.setText(ticker_list[11])
        self.edit3_3_1.setText(ticker_list[12])
        self.edit3_4_1.setText(ticker_list[13])
        self.edit3_5_1.setText(ticker_list[14])
        self.edit4_1_1.setText(ticker_list[15])
        self.edit4_2_1.setText(ticker_list[16])
        self.edit4_3_1.setText(ticker_list[17])
        self.edit4_4_1.setText(ticker_list[18])
        self.edit4_5_1.setText(ticker_list[19])
        self.edit5_1_1.setText(ticker_list[20])
        self.edit5_2_1.setText(ticker_list[21])
        self.edit5_3_1.setText(ticker_list[22])
        self.edit5_4_1.setText(ticker_list[23])
        self.edit5_5_1.setText(ticker_list[24])
        self.edit6_1_1.setText(ticker_list[25])
        self.edit6_2_1.setText(ticker_list[26])
        self.edit6_3_1.setText(ticker_list[27])
        self.edit6_4_1.setText(ticker_list[28])
        self.edit6_5_1.setText(ticker_list[29])
        self.edit7_1_1.setText(ticker_list[30])
        self.edit7_2_1.setText(ticker_list[31])
        self.edit7_3_1.setText(ticker_list[32])
        self.edit7_4_1.setText(ticker_list[33])
        self.edit7_5_1.setText(ticker_list[34])
        self.edit8_1_1.setText(ticker_list[35])
        self.edit8_2_1.setText(ticker_list[36])
        self.edit8_3_1.setText(ticker_list[37])
        self.edit8_4_1.setText(ticker_list[38])
        self.edit8_5_1.setText(ticker_list[39])
        self.edit9_1_1.setText(ticker_list[40])
        self.edit9_2_1.setText(ticker_list[41])
        self.edit9_3_1.setText(ticker_list[42])
        self.edit9_4_1.setText(ticker_list[43])
        self.edit9_5_1.setText(ticker_list[44])
        self.edit10_1_1.setText(ticker_list[45])
        self.edit10_2_1.setText(ticker_list[46])
        self.edit10_3_1.setText(ticker_list[47])
        self.edit10_4_1.setText(ticker_list[48])
        self.edit10_5_1.setText(ticker_list[49])
        self.edit11_1_1.setText(ticker_list[50])
        self.edit11_2_1.setText(ticker_list[51])
        self.edit11_3_1.setText(ticker_list[52])
        self.edit11_4_1.setText(ticker_list[53])
        self.edit11_5_1.setText(ticker_list[54])
        self.edit12_1_1.setText(ticker_list[55])
        self.edit12_2_1.setText(ticker_list[56])
        self.edit12_3_1.setText(ticker_list[57])
        self.edit12_4_1.setText(ticker_list[58])
        self.edit12_5_1.setText(ticker_list[59])

        self.edit1_1_1_2.setText(ticker_list[60])
        self.edit1_2_1_2.setText(ticker_list[61])
        self.edit1_3_1_2.setText(ticker_list[62])
        self.edit1_4_1_2.setText(ticker_list[63])
        self.edit1_5_1_2.setText(ticker_list[64])
        self.edit2_1_1_2.setText(ticker_list[65])
        self.edit2_2_1_2.setText(ticker_list[66])
        self.edit2_3_1_2.setText(ticker_list[67])
        self.edit2_4_1_2.setText(ticker_list[68])
        self.edit2_5_1_2.setText(ticker_list[69])
        self.edit3_1_1_2.setText(ticker_list[70])
        self.edit3_2_1_2.setText(ticker_list[71])
        self.edit3_3_1_2.setText(ticker_list[72])
        self.edit3_4_1_2.setText(ticker_list[73])
        self.edit3_5_1_2.setText(ticker_list[74])
        self.edit4_1_1_2.setText(ticker_list[75])
        self.edit4_2_1_2.setText(ticker_list[76])
        self.edit4_3_1_2.setText(ticker_list[77])
        self.edit4_4_1_2.setText(ticker_list[78])
        self.edit4_5_1_2.setText(ticker_list[79])
        self.edit5_1_1_2.setText(ticker_list[80])
        self.edit5_2_1_2.setText(ticker_list[81])
        self.edit5_3_1_2.setText(ticker_list[82])
        self.edit5_4_1_2.setText(ticker_list[83])
        self.edit5_5_1_2.setText(ticker_list[84])
        self.edit6_1_1_2.setText(ticker_list[85])
        self.edit6_2_1_2.setText(ticker_list[86])
        self.edit6_3_1_2.setText(ticker_list[87])
        self.edit6_4_1_2.setText(ticker_list[88])
        self.edit6_5_1_2.setText(ticker_list[89])
        self.edit7_1_1_2.setText(ticker_list[90])
        self.edit7_2_1_2.setText(ticker_list[91])
        self.edit7_3_1_2.setText(ticker_list[92])
        self.edit7_4_1_2.setText(ticker_list[93])
        self.edit7_5_1_2.setText(ticker_list[94])
        self.edit8_1_1_2.setText(ticker_list[95])
        self.edit8_2_1_2.setText(ticker_list[96])
        self.edit8_3_1_2.setText(ticker_list[97])
        self.edit8_4_1_2.setText(ticker_list[98])
        self.edit8_5_1_2.setText(ticker_list[99])
        self.edit9_1_1_2.setText(ticker_list[100])
        self.edit9_2_1_2.setText(ticker_list[101])
        self.edit9_3_1_2.setText(ticker_list[102])
        self.edit9_4_1_2.setText(ticker_list[103])
        self.edit9_5_1_2.setText(ticker_list[104])
        self.edit10_1_1_2.setText(ticker_list[105])
        self.edit10_2_1_2.setText(ticker_list[106])
        self.edit10_3_1_2.setText(ticker_list[107])
        self.edit10_4_1_2.setText(ticker_list[108])
        self.edit10_5_1_2.setText(ticker_list[109])
        self.edit11_1_1_2.setText(ticker_list[110])
        self.edit11_2_1_2.setText(ticker_list[111])
        self.edit11_3_1_2.setText(ticker_list[112])
        self.edit11_4_1_2.setText(ticker_list[113])
        self.edit11_5_1_2.setText(ticker_list[114])
        self.edit12_1_1_2.setText(ticker_list[115])
        self.edit12_2_1_2.setText(ticker_list[116])
        self.edit12_3_1_2.setText(ticker_list[117])
        self.edit12_4_1_2.setText(ticker_list[118])
        self.edit12_5_1_2.setText(ticker_list[119])


        self.edit1_1_2.setText(line_list[0])
        self.edit1_2_2.setText(line_list[1])
        self.edit1_3_2.setText(line_list[2])
        self.edit1_4_2.setText(line_list[3])
        self.edit1_5_2.setText(line_list[4])
        self.edit2_1_2.setText(line_list[5])
        self.edit2_2_2.setText(line_list[6])
        self.edit2_3_2.setText(line_list[7])
        self.edit2_4_2.setText(line_list[8])
        self.edit2_5_2.setText(line_list[9])
        self.edit3_1_2.setText(line_list[10])
        self.edit3_2_2.setText(line_list[11])
        self.edit3_3_2.setText(line_list[12])
        self.edit3_4_2.setText(line_list[13])
        self.edit3_5_2.setText(line_list[14])
        self.edit4_1_2.setText(line_list[15])
        self.edit4_2_2.setText(line_list[16])
        self.edit4_3_2.setText(line_list[17])
        self.edit4_4_2.setText(line_list[18])
        self.edit4_5_2.setText(line_list[19])
        self.edit5_1_2.setText(line_list[20])
        self.edit5_2_2.setText(line_list[21])
        self.edit5_3_2.setText(line_list[22])
        self.edit5_4_2.setText(line_list[23])
        self.edit5_5_2.setText(line_list[24])
        self.edit6_1_2.setText(line_list[25])
        self.edit6_2_2.setText(line_list[26])
        self.edit6_3_2.setText(line_list[27])
        self.edit6_4_2.setText(line_list[28])
        self.edit6_5_2.setText(line_list[29])
        self.edit7_1_2.setText(line_list[30])
        self.edit7_2_2.setText(line_list[31])
        self.edit7_3_2.setText(line_list[32])
        self.edit7_4_2.setText(line_list[33])
        self.edit7_5_2.setText(line_list[34])
        self.edit8_1_2.setText(line_list[35])
        self.edit8_2_2.setText(line_list[36])
        self.edit8_3_2.setText(line_list[37])
        self.edit8_4_2.setText(line_list[38])
        self.edit8_5_2.setText(line_list[39])
        self.edit9_1_2.setText(line_list[40])
        self.edit9_2_2.setText(line_list[41])
        self.edit9_3_2.setText(line_list[42])
        self.edit9_4_2.setText(line_list[43])
        self.edit9_5_2.setText(line_list[44])
        self.edit10_1_2.setText(line_list[45])
        self.edit10_2_2.setText(line_list[46])
        self.edit10_3_2.setText(line_list[47])
        self.edit10_4_2.setText(line_list[48])
        self.edit10_5_2.setText(line_list[49])
        self.edit11_1_2.setText(line_list[50])
        self.edit11_2_2.setText(line_list[51])
        self.edit11_3_2.setText(line_list[52])
        self.edit11_4_2.setText(line_list[53])
        self.edit11_5_2.setText(line_list[54])
        self.edit12_1_2.setText(line_list[55])
        self.edit12_2_2.setText(line_list[56])
        self.edit12_3_2.setText(line_list[57])
        self.edit12_4_2.setText(line_list[58])
        self.edit12_5_2.setText(line_list[59])




        self.edit1_1_2_2.setText(line_list[60])
        self.edit1_2_2_2.setText(line_list[61])
        self.edit1_3_2_2.setText(line_list[62])
        self.edit1_4_2_2.setText(line_list[63])
        self.edit1_5_2_2.setText(line_list[64])
        self.edit2_1_2_2.setText(line_list[65])
        self.edit2_2_2_2.setText(line_list[66])
        self.edit2_3_2_2.setText(line_list[67])
        self.edit2_4_2_2.setText(line_list[68])
        self.edit2_5_2_2.setText(line_list[69])
        self.edit3_1_2_2.setText(line_list[70])
        self.edit3_2_2_2.setText(line_list[71])
        self.edit3_3_2_2.setText(line_list[72])
        self.edit3_4_2_2.setText(line_list[73])
        self.edit3_5_2_2.setText(line_list[74])
        self.edit4_1_2_2.setText(line_list[75])
        self.edit4_2_2_2.setText(line_list[76])
        self.edit4_3_2_2.setText(line_list[77])
        self.edit4_4_2_2.setText(line_list[78])
        self.edit4_5_2_2.setText(line_list[79])
        self.edit5_1_2_2.setText(line_list[80])
        self.edit5_2_2_2.setText(line_list[81])
        self.edit5_3_2_2.setText(line_list[82])
        self.edit5_4_2_2.setText(line_list[83])
        self.edit5_5_2_2.setText(line_list[84])
        self.edit6_1_2_2.setText(line_list[85])
        self.edit6_2_2_2.setText(line_list[86])
        self.edit6_3_2_2.setText(line_list[87])
        self.edit6_4_2_2.setText(line_list[88])
        self.edit6_5_2_2.setText(line_list[89])
        self.edit7_1_2_2.setText(line_list[90])
        self.edit7_2_2_2.setText(line_list[91])
        self.edit7_3_2_2.setText(line_list[92])
        self.edit7_4_2_2.setText(line_list[93])
        self.edit7_5_2_2.setText(line_list[94])
        self.edit8_1_2_2.setText(line_list[95])
        self.edit8_2_2_2.setText(line_list[96])
        self.edit8_3_2_2.setText(line_list[97])
        self.edit8_4_2_2.setText(line_list[98])
        self.edit8_5_2_2.setText(line_list[99])
        self.edit9_1_2_2.setText(line_list[100])
        self.edit9_2_2_2.setText(line_list[101])
        self.edit9_3_2_2.setText(line_list[102])
        self.edit9_4_2_2.setText(line_list[103])
        self.edit9_5_2_2.setText(line_list[104])
        self.edit10_1_2_2.setText(line_list[105])
        self.edit10_2_2_2.setText(line_list[106])
        self.edit10_3_2_2.setText(line_list[107])
        self.edit10_4_2_2.setText(line_list[108])
        self.edit10_5_2_2.setText(line_list[109])
        self.edit11_1_2_2.setText(line_list[110])
        self.edit11_2_2_2.setText(line_list[111])
        self.edit11_3_2_2.setText(line_list[112])
        self.edit11_4_2_2.setText(line_list[113])
        self.edit11_5_2_2.setText(line_list[114])
        self.edit12_1_2_2.setText(line_list[115])
        self.edit12_2_2_2.setText(line_list[116])
        self.edit12_3_2_2.setText(line_list[117])
        self.edit12_4_2_2.setText(line_list[118])
        self.edit12_5_2_2.setText(line_list[119])

    def val_change(self):
        self.edit1_t = self.edit1.text()
        self.edit2_t = self.edit2.text()
        self.edit3_t = self.edit3.text()
        self.edit4_t = self.edit4.text()
        self.edit5_t = self.edit5.text()
        self.edit6_t = self.edit6.text()
        self.edit7_t = self.edit7.text()
        pass
def df_date(df,date):
    # df.index = df.index.astype(str)
    # df.loc[df.index,'날짜'] = df.index.str[4:8] ##index에서 str짤라가지고 date컬럼 생성
    df['날짜'] = df.index  ##index에서 str짤라가지고 '시간'컬럼 생성
    df['년도'] = df['날짜'].astype(str).str[:4]
    if (df['년도']==date).any(): #'날짜'컬럼에 date가 포함되는지 여부, all() 사용 시 -모든값이 date인지
        df = df[df.년도 == date]  # date변수와 일치하는 'date'컬럼 값 만 df에 저장
        # print(df)
    else:
        df = pd.DataFrame()
        print('일치하는 날짜 없음')
    return df
def split_time(df,start,end):
    start = int(start) #시작시간을 정수형으로 변환
    if end == 'now':
        end = datetime.datetime.now().strftime("%Y%m%d")
    end = int(end) #끝시간을 정수형으로 변환
    # df.index = df.index.astype(str)
    df['날짜'] = df.index.astype(int)  ##index에서 str짤라가지고 '시간'컬럼 생성
    # df = df.astype({'시간':'int'}) #'시간'컬럼을 int형으로 변환
    df = df[df.날짜 >= start]
    df = df[df.날짜 <= end]
    df['년도'] = df['날짜'].astype(str).str[:4]
    groups = df.groupby('년도') #날짜별 그룹 만들기
    return df,groups
def qtable_moneytop(file):

    con = sqlite3.connect(file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list=cursor.fetchall() #fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
    if not table_list:
        print('* DB 테이블이 비어있음 - 확인 필요 *')
    table_list = np.concatenate(table_list).tolist() #모든테이블을 리스트로변환 https://codechacha.com/ko/python-flatten-list/
    df_macro=pd.DataFrame()
    for i,table in enumerate(table_list):
        df = pd.read_sql("SELECT * FROM '"+ table+"'", con).set_index('index')
        df,groups = split_time(df, start, end)
        df_groups = groups.size()
        # df_groups=Series(index = table)
        # print(df_groups)
        # quit()
        # df_groups = df_groups.transpose()
        df_macro = pd.concat([df_macro,df_groups],axis=1)
        # print(df_macro)
        # df_macro.
    df_macro.columns = table_list
    df_macro = df_macro.transpose() #행,열 바꾸기
    df_macro['종목'] = df_macro.index
    col1 = df_macro.columns[-1:].to_list() #컬럼 순서 바꾸기
    col2 = df_macro.columns[:-1].to_list()
    df_macro = df_macro[col1+col2]
    return df_macro
def qtable_back_list(select):
    con = sqlite3.connect(back_file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
    if not table_list:
        print('* DB 테이블이 비어있음 - 확인 필요 *')
    table_list = np.concatenate(table_list).tolist()  # 모든테이블을 리스트로변환 https://codechacha.com/ko/python-flatten-list/
    # print(table_list)
    table = ''
    if select == 'vj':
        table = 'stock_vj' #백테스트 불러오기
        print('vj 불러오기')
    elif select == 'vc':
        table = 'stock_vc' #최적화 불러오기
        print('vc 불러오기')
    df = pd.read_sql("SELECT * FROM '"+table+"'", con).set_index('index')
    # print(df)
    df.index = df.index.astype(str)
    df['index'] = df.index.str[4:6]+'/'+df.index.str[6:8]+' '+df.index.str[8:10]+':'+df.index.str[10:12] #db테이블의 테이블 제목이랑 stock_vj의 index가 다름 주의
    df['index'] = df.index

    # print('back 컬럼명=',df.columns.tolist())
    if select == 'vj':
        df = df[['index', '평균수익률', '승률', '최대낙폭률', '일평균거래횟수', '최대보유종목수', '수익률합계', '수익금합계', '거래횟수', '필요자금', '배팅금액', '평균보유기간',
                 '익절', '손절','매수전략', '매도전략'
                 ]]
    elif select == 'vc':
        df = df[['index', '평균수익률', '승률', '최대낙폭률', '일평균거래횟수', '최대보유종목수', '수익률합계', '수익금합계', '거래횟수','필요자금', '배팅금액', '평균보유기간',
                 '익절', '손절', '변수','매수전략', '매도전략', '범위설정']]
    # print(df)
    con.close()
    return df
def qtable_backtest(v_time,cap,ohlcv,fun):
    def backtest(v_time):
        # print(v_time)
        con = sqlite3.connect(back_file)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        back_table_list = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기
        back_table_list = np.concatenate(back_table_list).tolist()  # 모든테이블을 리스트로변환 https://codechacha.com/ko/python-flatten-list/
        # print(back_table_list)
        v_table = [x for x in back_table_list if str(x)[-14:-2] == str(v_time)[:-2]] #백리스트 목록에서 입력받은 값과 같은거 찾기
        # print('vtable',v_table)
        back_table = v_table[0]
        # print(type(back_table))
        df_back_list = pd.read_sql("SELECT * FROM " + back_table, con).set_index('index')
        # print(df_back_list)
        df_back_list = df_time(df_back_list, start, end)  # 백테스트 시간 슬라이싱
        con.close()
        dict_bt = df_back_list['종목명'].to_dict()
        bt_list = list(set(';'.join(list(dict_bt.values())).split(';')))
        stock_name = df_back_list['종목명'].str.split(';').apply(Series, 1).stack()
        buy_time = df_back_list['매수시간'].str.split(';').apply(Series, 1).stack()
        sell_time = df_back_list['매도시간'].str.split(';').apply(Series, 1).stack()
        buy_price = df_back_list['매수가'].str.split(';').apply(Series, 1).stack()
        sell_price = df_back_list['매도가'].str.split(';').apply(Series, 1).stack()
        profit = df_back_list['수익률'].str.split(';').apply(Series, 1).stack()
        stock_name.index = stock_name.index.droplevel(-1)  # to line up with df_back_list's index
        buy_time.index = buy_time.index.droplevel(-1)  # to line up with df_back_list's index
        sell_time.index = sell_time.index.droplevel(-1)  # to line up with df_back_list's index
        buy_price.index = buy_price.index.droplevel(-1)  # to line up with df_back_list's index
        sell_price.index = sell_price.index.droplevel(-1)  # to line up with df_back_list's index
        profit.index = profit.index.droplevel(-1)  # to line up with df_back_list's index
        stock_name.name = '종목명'  # needs a name to join
        buy_time.name = '매수시간'  # needs a name to join
        sell_time.name = '매도시간'  # needs a name to join
        buy_price.name = '매수가'  # needs a name to join
        sell_price.name = '매도가'  # needs a name to join
        profit.name = '수익률'  # needs a name to join
        del df_back_list['종목명']
        del df_back_list['매수시간']
        del df_back_list['매도시간']
        del df_back_list['매수가']
        del df_back_list['매도가']
        del df_back_list['수익률']
        del df_back_list['시간']
        del df_back_list['수익금']
        del df_back_list['수익금합계']
        df = pd.DataFrame()
        df = pd.concat([stock_name, buy_time, sell_time, buy_price, sell_price, profit], axis=1)  # 시리즈를 열방향으로 합치기
        df['매수시간'] = pd.to_numeric(df['매수시간'])
        df['매도시간'] = pd.to_numeric(df['매도시간'])
        df[['수익률']] = df[['수익률']].astype(float)  # 수익률 컬럼 float으로 변환
        df['보유시간'] = df['매도시간'] - df['매수시간']
        df['청산횟수'] = df.groupby(['종목명']).매수시간.transform('count') #종목명이 같은그룹을 매수시간 기준으로 카운트
        df['날짜'] = df.index.str[0:8] ##index에서 str짤라가지고 date컬럼 생성
        df['당일청산'] = df.groupby(['종목명', '날짜']).날짜.transform('count') #종목명,날짜가 같은그룹을 날짜 기준으로 카운트
        df['전체수익'] = df.groupby(['종목명']).수익률.transform('sum') #종목명,날짜가 같은그룹을 수익률 기준으로 합산
        df['당일수익'] = df.groupby(['종목명', '날짜']).수익률.transform('sum')
        # print(df)
        for stock_name in df['종목명']:
            stock_code = make_stock_code(stock_name)
            df.loc[df.종목명 == stock_name, '종목코드'] = stock_code
        df['전일날짜'] = (df['매수시간'] - 1000000).astype(str).str[0:8]  # -1000000넣는 이유는 전일 기준으로 하기위해
        df = df[['종목코드','종목명','수익률','당일수익','전체수익','보유시간','당일청산','청산횟수','전일날짜','매수시간','매도시간','매수가','매도가' ]]
        # df.to_excel("D:/PythonProjects/df_sort.xlsx")
        return df
    def backtest_cap(df):
        df_del = df[['종목코드','전일날짜']]
        groups = df_del.groupby('전일날짜')
        df_back = pd.DataFrame() #빈프레임
        days = list(groups.size().index)
        for day in days:  # 날짜 그룹별로 접근(종가,시총,거래량,거래대금,주식수)
            df_db_date = df_del[df_del.전일날짜 == day]  # 날짜가 같은 데이터만 df_db로 불러옴
            df_cap = stock.get_market_cap(day)
            df_cap.reset_index(drop=False, inplace=True)  # 인덱스 번호순 으로 재 정의
            df_cap.rename(columns={'티커': '종목코드'}, inplace=True)  # 컬럼명 변경
            df_db_date = pd.merge(df_db_date, df_cap, how='left', left_on='종목코드', right_on='종목코드') # 종목코드 기준으로 합치기 pykrx에서 가져온 정보 넣기
            df_back = pd.concat([df_back, df_db_date])
        df_back.drop(['종목코드','전일날짜','종가','거래량','거래대금'], axis=1,inplace=True)  # 중복되고 필요없는 열 삭제
        df_back['시가총액'] = round(df_back['시가총액']/100000000,1)
        df_back['상장주식수'] = round(df_back['상장주식수']/1000000,1)
        df_back.rename(columns={'시가총액':'전일시총(억)','상장주식수':'주식수(백만)'}, inplace=True)  # 컬럼명 변경
        df.reset_index(drop=True, inplace=True)  #서로 합치기 위해 인덱스를 재정의하여 맞춰줌
        df_back.reset_index(drop=True, inplace=True)  #서로 합치기 위해 인덱스를 재정의하여 맞춰줌
        df_back = pd.concat([df, df_back],axis=1)
        return df_back
    def backtest_ohlcv(df):
        df_del = df[['종목코드','전일날짜']]
        groups = df_del.groupby('전일날짜')
        df_back = pd.DataFrame() #빈프레임
        days = list(groups.size().index)
        for day in days:  # 날짜 그룹별로 접근(ohlcv)
            df_db_date = df_del[df_del.전일날짜 == day]  # 날짜가 같은 데이터만 df_db로 불러옴
            df_cap = stock.get_market_ohlcv(day,market='ALL')
            df_cap.reset_index(drop=False, inplace=True)  # 인덱스 번호순 으로 재 정의
            df_cap.rename(columns={'티커': '종목코드'}, inplace=True)  # 컬럼명 변경
            df_db_date = pd.merge(df_db_date, df_cap, how='left', left_on='종목코드', right_on='종목코드') # 종목코드 기준으로 합치기 pykrx에서 가져온 정보 넣기
            df_back = pd.concat([df_back, df_db_date])
        df_back.drop(['종목코드','전일날짜'], axis=1,inplace=True)  # 중복되고 필요없는 열 삭제
        df_back['거래량'] = round(df_back['거래량']/1000000,1)
        df_back['거래대금'] = round(df_back['거래대금']/100000000,1)
        df_back['전일고저'] = round(((df_back['고가']-df_back['저가'])/df_back['저가'])*100,2)
        df_back.rename(columns={'시가':'전일시가','고가': '전일고가','저가': '전일저가','종가': '전일종가','거래량':'전거래량(백만)','거래대금':'전거래대금(억)','등락률':'전일등락'}, inplace=True)  # 컬럼명 변경
        df.reset_index(drop=True, inplace=True)  #서로 합치기 위해 인덱스를 재정의하여 맞춰줌
        df_back.reset_index(drop=True, inplace=True)  #서로 합치기 위해 인덱스를 재정의하여 맞춰줌
        df_back = pd.concat([df, df_back],axis=1)
        return df_back
    def backtest_fun(df):
        df_del = df[['종목코드','전일날짜']]
        groups = df_del.groupby('전일날짜')
        df_back = pd.DataFrame() #빈프레임
        days = list(groups.size().index)
        for day in days:  # 날짜 그룹별로 접근(펀더멘탈)
            df_db_date = df_del[df_del.전일날짜 == day]  # 날짜가 같은 데이터만 df_db로 불러옴
            df_cap = stock.get_market_fundamental(day,market='ALL')
            df_cap.reset_index(drop=False, inplace=True)  # 인덱스 번호순 으로 재 정의
            df_cap.rename(columns={'티커': '종목코드'}, inplace=True)  # 컬럼명 변경
            df_db_date = pd.merge(df_db_date, df_cap, how='left', left_on='종목코드', right_on='종목코드') # 종목코드 기준으로 합치기 pykrx에서 가져온 정보 넣기
            df_back = pd.concat([df_back, df_db_date])
        df_back.drop(['종목코드','전일날짜'], axis=1,inplace=True)  # 중복되고 필요없는 열 삭제
        df.reset_index(drop=True, inplace=True)  #서로 합치기 위해 인덱스를 재정의하여 맞춰줌
        df_back.reset_index(drop=True, inplace=True)  #서로 합치기 위해 인덱스를 재정의하여 맞춰줌
        df_back = pd.concat([df, df_back],axis=1)
        return df_back
    df = backtest(v_time)
    # print(df)
    if cap == True:
        df = backtest_cap(df)
    if ohlcv == True:
        df = backtest_ohlcv(df)
    if fun == True:
        df = backtest_fun(df)
    # print(df)
    df.drop(['전일날짜'], axis=1, inplace=True)  # 중복되거나 필요없는 열 삭제
    # print('back 컬럼명=',df.columns.tolist())
    # print(df.sort_values(by=['매수시간']))
    return df
def stock_infomation(stock_code):
    stock_code = make_stock_code(stock_code)
    stock_name = make_stock_name(stock_code)
    stock_info = stock_list.loc[stock_list['회사명'] == stock_name]
    print(stock_info)
    return stock_code,stock_name
def make_stock_name(stock_code):
    stock_info = stock_list.loc[stock_list['종목코드'] == stock_code]
    stock_name = stock_info.iloc[0]['회사명']  # 회사명으로 변환
    return stock_name
def make_stock_code(stock_name):
    try:
        stock_info = stock_list.loc[stock_list['회사명'] == stock_name]
        stock_code = stock_info.iloc[0]['종목코드']  # 종목코드로 변환
    except:
        stock_info = stock_list2.loc[stock_list2['종목명'] == stock_name]
        # print(stock_info)
        stock_code = stock_info.iloc[0]['종목코드']  # 종목코드로 변환
    return stock_code
def get_data(stock_code,date,file):
    if not os.path.isfile(file):
        print('* 파일 없음 - 경로 확인 *')
    con = sqlite3.connect(file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    try:
        df = pd.read_sql("SELECT * FROM " + "'" + stock_code + "'", con).set_index('index')
    except:
        print('* db파일에 종목 없음 *')
        df = []
    df = df_date(df, date)
    if df.empty:
        print('* db테이블에 종목은 있으나 데이터가 비어있음 또는 머니탑에 종목은 있으나 테이블이 비어있음- 확인 필요 *')

    con.close()
    return df
def get_table_list(file):
    con = sqlite3.connect(file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
    if not table_list:
        print('* DB 테이블이 비어있음 - 확인 필요 *')
    table_list = np.concatenate(table_list).tolist()  # 모든테이블을 리스트로변환 https://codechacha.com/ko/python-flatten-list/
    # print(table_list)
    return table_list

def db_stock_list():
    con = sqlite3.connect(stock_tick_file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table = 'codename'
    df = pd.read_sql("SELECT * FROM " + "'" + table + "'", con).set_index('index')
    # df['종목코드'] = df.index
    con.close()
    df.reset_index(drop=False, inplace=True)  # 인덱스 번호순 으로 재 정의
    df.rename(columns={'index': '종목코드'}, inplace=True)  # 컬럼명 변경
    return df
class Chart(QWidget):
    def __init__(self,df,date):
    # def __init__(self):
        super().__init__()
        # self.win = pg.GraphicsLayoutWidget(show=True)
        self.win1 = pg.GraphicsLayoutWidget(self) #pyqtgraph
        self.win2 = pg.GraphicsLayoutWidget(self) #pyqtgraph

        tabs = QTabWidget()
        tabs.addTab(self.win1, 'Tab1')
        tabs.addTab(self.win2, 'Tab2')
        # self.table = QTableWidget(self)
        # self.plaintext = QPlainTextEdit(self)
        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)
        vbox.setContentsMargins(0,0,0,0)

        # self.win1.setWindowTitle('주식차트')
        # self.win2.setWindowTitle('주식차트')
        self.win1.setGeometry(0, 0, 3850, 1010)
        self.win2.setGeometry(0, 0, 3850, 1010)
        bottomAxis_1 = pg.AxisItem(orientation='bottom')
        bottomAxis_2 = pg.AxisItem(orientation='bottom')
        bottomAxis_date_1 = pg.AxisItem(orientation='bottom')
        bottomAxis_date_2 = pg.AxisItem(orientation='bottom')

        # link_view
        area = DockArea()
        # d1 = Dock("Dock1")
        area.addDock(Dock("Dock1"), 'bottom')

        df_list = df.columns.tolist()

        # p1_1 = self.win.addPlot(row=0, col=0,title=stock_name + date,axisItems={'bottom': pg.DateAxisItem()})
        # p1_2 = self.win.addPlot(row=1, col=0,title='체결강도',axisItems={'bottom': pg.AxisItem(orientation='bottom')})
        p1_1  = self.win1.addPlot(row=0, col=0,title=f'{df_list[0]}_{date}',axisItems={'bottom': pg.DateAxisItem()})
        p1_2  = self.win1.addPlot(row=1, col=0,title=f'{df_list[5]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_3  = self.win1.addPlot(row=2, col=0,title=f'{df_list[10]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_4  = self.win1.addPlot(row=0, col=1,title=f'{df_list[15]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_5  = self.win1.addPlot(row=1, col=1,title=f'{df_list[20]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_6  = self.win1.addPlot(row=2, col=1,title=f'{df_list[25]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_7  = self.win1.addPlot(row=0, col=2,title=f'{df_list[30]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_8  = self.win1.addPlot(row=1, col=2,title=f'{df_list[35]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_9  = self.win1.addPlot(row=2, col=2,title=f'{df_list[40]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_10 = self.win1.addPlot(row=0, col=3,title=f'{df_list[45]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_11 = self.win1.addPlot(row=1, col=3,title=f'{df_list[50]}',axisItems={'bottom': pg.DateAxisItem()})
        p1_12 = self.win1.addPlot(row=2, col=3,title=f'{df_list[55]}',axisItems={'bottom': pg.DateAxisItem()})


        p2_1  = self.win2.addPlot(row=0, col=0, title=f'{df_list[60]}_{date}',axisItems={'bottom': pg.DateAxisItem()})
        p2_2  = self.win2.addPlot(row=1, col=0, title=f'{df_list[65]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_3  = self.win2.addPlot(row=2, col=0, title=f'{df_list[70]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_4  = self.win2.addPlot(row=0, col=1, title=f'{df_list[75]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_5  = self.win2.addPlot(row=1, col=1, title=f'{df_list[80]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_6  = self.win2.addPlot(row=2, col=1, title=f'{df_list[85]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_7  = self.win2.addPlot(row=0, col=2, title=f'{df_list[90]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_8  = self.win2.addPlot(row=1, col=2, title=f'{df_list[95]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_9  = self.win2.addPlot(row=2, col=2, title=f'{df_list[100]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_10 = self.win2.addPlot(row=0, col=3, title=f'{df_list[105]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_11 = self.win2.addPlot(row=1, col=3, title=f'{df_list[110]}', axisItems={'bottom': pg.DateAxisItem()})
        p2_12 = self.win2.addPlot(row=2, col=3, title=f'{df_list[115]}', axisItems={'bottom': pg.DateAxisItem()})

        p1_1.addLegend()
        p1_2.addLegend()
        p1_3.addLegend()
        p1_4.addLegend()
        p1_5.addLegend()
        p1_6.addLegend()
        p1_7.addLegend()
        p1_8.addLegend()
        p1_9.addLegend()
        p1_10.addLegend()
        p1_11.addLegend()
        p1_12.addLegend()

        p2_1.addLegend()
        p2_2.addLegend()
        p2_3.addLegend()
        p2_4.addLegend()
        p2_5.addLegend()
        p2_6.addLegend()
        p2_7.addLegend()
        p2_8.addLegend()
        p2_9.addLegend()
        p2_10.addLegend()
        p2_11.addLegend()
        p2_12.addLegend()

        p1_1.showGrid(x=True, y=True)
        # d1.addWidget(p1_1)
        p1_2.showGrid(x=True, y=True)
        p1_3.showGrid(x=True, y=True)
        p1_4.showGrid(x=True, y=True)
        p1_5.showGrid(x=True, y=True)
        p1_6.showGrid(x=True, y=True)
        p1_7.showGrid(x=True, y=True)
        p1_8.showGrid(x=True, y=True)
        p1_9.showGrid(x=True, y=True)
        p1_10.showGrid(x=True, y=True)
        p1_11.showGrid(x=True, y=True)
        p1_12.showGrid(x=True, y=True)

        p2_1.showGrid(x=True, y=True)
        p2_2.showGrid(x=True, y=True)
        p2_3.showGrid(x=True, y=True)
        p2_4.showGrid(x=True, y=True)
        p2_5.showGrid(x=True, y=True)
        p2_6.showGrid(x=True, y=True)
        p2_7.showGrid(x=True, y=True)
        p2_8.showGrid(x=True, y=True)
        p2_9.showGrid(x=True, y=True)
        p2_10.showGrid(x=True, y=True)
        p2_11.showGrid(x=True, y=True)
        p2_12.showGrid(x=True, y=True)

        p1_2.setXLink(p1_1)
        p1_3.setXLink(p1_1)
        p1_4.setXLink(p1_1)
        p1_5.setXLink(p1_1)
        p1_6.setXLink(p1_1)
        p1_7.setXLink(p1_1)
        p1_8.setXLink(p1_1)
        p1_9.setXLink(p1_1)
        p1_10.setXLink(p1_1)
        p1_11.setXLink(p1_1)
        p1_12.setXLink(p1_1)

        p2_2.setXLink(p2_1)
        p2_3.setXLink(p2_1)
        p2_4.setXLink(p2_1)
        p2_5.setXLink(p2_1)
        p2_6.setXLink(p2_1)
        p2_7.setXLink(p2_1)
        p2_8.setXLink(p2_1)
        p2_9.setXLink(p2_1)
        p2_10.setXLink(p2_1)
        p2_11.setXLink(p2_1)
        p2_12.setXLink(p2_1)

        self.win1.ci.layout.setColumnStretchFactor(0, 100)
        self.win1.ci.layout.setColumnStretchFactor(1, 105)
        self.win1.ci.layout.setColumnStretchFactor(2, 105)
        self.win1.ci.layout.setColumnStretchFactor(3,  85)

        self.win2.ci.layout.setColumnStretchFactor(0, 100)
        self.win2.ci.layout.setColumnStretchFactor(1, 105)
        self.win2.ci.layout.setColumnStretchFactor(2, 105)
        self.win2.ci.layout.setColumnStretchFactor(3, 85)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # # Basic Array Plotting
        p1_1.clear()
        p1_2.clear()
        p1_3.clear()
        p1_4.clear()
        p1_5.clear()
        p1_6.clear()
        p1_7.clear()
        p1_8.clear()
        p1_9.clear()
        p1_10.clear()
        p1_11.clear()
        p1_12.clear()

        p2_1.clear()
        p2_2.clear()
        p2_3.clear()
        p2_4.clear()
        p2_5.clear()
        p2_6.clear()
        p2_7.clear()
        p2_8.clear()
        p2_9.clear()
        p2_10.clear()
        p2_11.clear()
        p2_12.clear()


        # xticks = [x.timestamp() - 32400 for x in df.index]
        df['index_time'] = pd.to_datetime(df.index, format='%Y%m%d')
        df = df.astype({'index_time': 'str'})
        df=df.drop_duplicates(['index_time']) #시간이 중복인 행 제거
        df.loc[df.index, 'index_time'] = df[df.index_time.str[-2:] == '00']   # index_chart의 초가 '00'인 경우만 index_chart컬럼 값 저장
        df = df.astype({'index_time': 'str'}) #'index_time'컬럼을 str로 변환
        df['index_time'] = df['index_time'].str[11:-3]

        df['index_date'] = pd.to_datetime(df.index, format='%Y%m%d')
        df = df.astype({'index_date': 'str'})

        # p = df.index[df['날짜']!=df['날짜'].shift(1)] # 날짜가 바뀌는 행의 인덱스를 추출
        # df['index_date'] = df.loc[p,'index_date'] #추출한 인덱스값의 'index_date'컬럼 값만 남김
        df['index_date'] = df['index_date'].str[5:11]
        df['index_date'] = df['index_date'].replace(np.nan,'',regex=True) #nan값을 공백으로 변경

        df['index_chart']=df['index_date']+df['index_time'] #더하기
        df['index_chart'] = df['index_chart'].str[0:5]
        df['index_chart'] = df['index_chart'].replace(end,'',regex=True) #차트의 마지막 index 값을 공백으로 변경
        # df['매수가'] = df['매수가'].replace(np.nan,'',regex=True) #nan값을 공백으로 변경

        df['number'] = range(0,len(df)) # 넘버링 컬럼 추가
        # print(df)
        # buy_index = df['number'][df['매수가'].isna() == False] #'매수가'가 nan이 아닌 행의 'number' 컬럼 값을 추출
        # buy_price = df['매수가'][df['매수가'].isna() == False] #'매수가'가 nan이 아닌 행의 '매수가' 컬럼의 값을 추출
        # sell_index = df['number'][df['매도가'].isna() == False] #'매도가'가 nan이 아닌 행의 'number' 컬럼 값을 추출
        # sell_price = df['매도가'][df['매도가'].isna() == False] #'매도가'가 nan이 아닌 행의 '매도가' 컬럼의 값을 추출

        time = df['index_chart'].tolist()
        xDict=dict(enumerate(time))
        xValue=list(xDict.keys())
        xtickts=[xDict.items()]
        bottomAxis_1.setTicks(xtickts)
        bottomAxis_2.setTicks(xtickts)

        date = df['index_date'].tolist()
        xDict=dict(enumerate(date))
        xDate=list(xDict.keys())
        xtickts_date=[xDict.items()]
        bottomAxis_date_1.setTicks(xtickts_date)
        bottomAxis_date_2.setTicks(xtickts_date)

        df.index = pd.to_datetime(df.index, format='%Y%m%d')  # index를 df['index_time']컬럼의 datetime64 타입으로 저장 2022-01-05
        xValue = [int(x.timestamp()) - 32400 for x in df.index]
        # print(df)

        y_dot = pg.mkPen(color='y', width=1, style=QtCore.Qt.DotLine)
        g_dot = pg.mkPen(color='g', width=1, style=QtCore.Qt.DotLine)
        w_dot = pg.mkPen(color='w', width=1, style=QtCore.Qt.DotLine)
        r_dash = pg.mkPen(color='r', width=1, style=QtCore.Qt.DashLine)
        g_dash = pg.mkPen(color=[0,130,153], width=1.2, style=QtCore.Qt.DashLine)

        # p1_1.plot(x=buy_index, y=buy_price,   pen =None, symbolBrush =(200,  0,  0),symbolPen ='w', symbol='t' , symbolSize=10, name="진입") #마커
        # p1_1.plot(x=sell_index, y=sell_price, pen =None, symbolBrush =(  0,  0,200),symbolPen ='w', symbol='t1', symbolSize=10, name="청산") #마커
        # lr = pg.LinearRegionItem([50, 100])
        # lr.setZValue(-1)
        # p1_1.addItem(lr)

        p1_1.plot(x=xValue,  y=df[f'{df_list[0]}'], pen=(204, 61, 61),name=f'{df_list[0]}')
        p1_1.plot(x=xValue,  y=df[f'{df_list[1]}'], pen=(204,166, 61),name=f'{df_list[1]}')
        p1_1.plot(x=xValue,  y=df[f'{df_list[2]}'], pen=(159,201, 60),name=f'{df_list[2]}')
        p1_1.plot(x=xValue,  y=df[f'{df_list[3]}'], pen=( 61,183,204),name=f'{df_list[3]}')
        p1_1.plot(x=xValue,  y=df[f'{df_list[4]}'], pen=(128, 65,217),name=f'{df_list[4]}')
        p1_2.plot(x=xValue,  y=df[f'{df_list[5]}'], pen=(204, 61, 61),name=f'{df_list[5]}')
        p1_2.plot(x=xValue,  y=df[f'{df_list[6]}'], pen=(204,166, 61),name=f'{df_list[6]}')
        p1_2.plot(x=xValue,  y=df[f'{df_list[7]}'], pen=(159,201, 60),name=f'{df_list[7]}')
        p1_2.plot(x=xValue,  y=df[f'{df_list[8]}'], pen=( 61,183,204),name=f'{df_list[8]}')
        p1_2.plot(x=xValue,  y=df[f'{df_list[9]}'], pen=(128, 65,217),name=f'{df_list[9]}')
        p1_3.plot(x=xValue,  y=df[f'{df_list[10]}'], pen=(204, 61, 61), name=f'{df_list[10]}')
        p1_3.plot(x=xValue,  y=df[f'{df_list[11]}'], pen=(204,166, 61), name=f'{df_list[11]}')
        p1_3.plot(x=xValue,  y=df[f'{df_list[12]}'], pen=(159,201, 60), name=f'{df_list[12]}')
        p1_3.plot(x=xValue,  y=df[f'{df_list[13]}'], pen=( 61,183,204), name=f'{df_list[13]}')
        p1_3.plot(x=xValue,  y=df[f'{df_list[14]}'], pen=(128, 65,217), name=f'{df_list[14]}')
        p1_4.plot(x=xValue,  y=df[f'{df_list[15]}'], pen=(204, 61, 61), name=f'{df_list[15]}')
        p1_4.plot(x=xValue,  y=df[f'{df_list[16]}'], pen=(204,166, 61), name=f'{df_list[16]}')
        p1_4.plot(x=xValue,  y=df[f'{df_list[17]}'], pen=(159,201, 60), name=f'{df_list[17]}')
        p1_4.plot(x=xValue,  y=df[f'{df_list[18]}'], pen=( 61,183,204), name=f'{df_list[18]}')
        p1_4.plot(x=xValue,  y=df[f'{df_list[19]}'], pen=(128, 65,217), name=f'{df_list[19]}')
        p1_5.plot(x=xValue,  y=df[f'{df_list[20]}'], pen=(204, 61, 61), name=f'{df_list[20]}')
        p1_5.plot(x=xValue,  y=df[f'{df_list[21]}'], pen=(204,166, 61), name=f'{df_list[21]}')
        p1_5.plot(x=xValue,  y=df[f'{df_list[22]}'], pen=(159,201, 60), name=f'{df_list[22]}')
        p1_5.plot(x=xValue,  y=df[f'{df_list[23]}'], pen=( 61,183,204), name=f'{df_list[23]}')
        p1_5.plot(x=xValue,  y=df[f'{df_list[24]}'], pen=(128, 65,217), name=f'{df_list[24]}')
        p1_6.plot(x=xValue,  y=df[f'{df_list[25]}'], pen=(204, 61, 61), name=f'{df_list[25]}')
        p1_6.plot(x=xValue,  y=df[f'{df_list[26]}'], pen=(204, 166, 61), name=f'{df_list[26]}')
        p1_6.plot(x=xValue,  y=df[f'{df_list[27]}'], pen=(159, 201, 60), name=f'{df_list[27]}')
        p1_6.plot(x=xValue,  y=df[f'{df_list[28]}'], pen=(61, 183, 204), name=f'{df_list[28]}')
        p1_6.plot(x=xValue,  y=df[f'{df_list[29]}'], pen=(128, 65, 217), name=f'{df_list[29]}')
        p1_7.plot(x=xValue,  y=df[f'{df_list[30]}'], pen=(204, 61, 61), name=f'{df_list[30]}')
        p1_7.plot(x=xValue,  y=df[f'{df_list[31]}'], pen=(204, 166, 61), name=f'{df_list[31]}')
        p1_7.plot(x=xValue,  y=df[f'{df_list[32]}'], pen=(159, 201, 60), name=f'{df_list[32]}')
        p1_7.plot(x=xValue,  y=df[f'{df_list[33]}'], pen=(61, 183, 204), name=f'{df_list[33]}')
        p1_7.plot(x=xValue,  y=df[f'{df_list[34]}'], pen=(128, 65, 217), name=f'{df_list[34]}')
        p1_8.plot(x=xValue,  y=df[f'{df_list[35]}'], pen=(204, 61, 61), name=f'{df_list[35]}')
        p1_8.plot(x=xValue,  y=df[f'{df_list[36]}'], pen=(204,166, 61), name=f'{df_list[36]}')
        p1_8.plot(x=xValue,  y=df[f'{df_list[37]}'], pen=(159,201, 60), name=f'{df_list[37]}')
        p1_8.plot(x=xValue,  y=df[f'{df_list[38]}'], pen=( 61, 183,204), name=f'{df_list[38]}')
        p1_8.plot(x=xValue,  y=df[f'{df_list[39]}'], pen=(128, 65, 217), name=f'{df_list[39]}')
        p1_9.plot(x=xValue,  y=df[f'{df_list[40]}'], pen=(204, 61, 61), name=f'{df_list[40]}')
        p1_9.plot(x=xValue,  y=df[f'{df_list[41]}'], pen=(204, 166, 61), name=f'{df_list[41]}')
        p1_9.plot(x=xValue,  y=df[f'{df_list[42]}'], pen=(159, 201, 60), name=f'{df_list[42]}')
        p1_9.plot(x=xValue,  y=df[f'{df_list[43]}'], pen=(61, 183, 204), name=f'{df_list[43]}')
        p1_9.plot(x=xValue,  y=df[f'{df_list[44]}'], pen=(128, 65, 217), name=f'{df_list[44]}')
        p1_10.plot(x=xValue, y=df[f'{df_list[45]}'], pen=(204, 61, 61), name=f'{df_list[45]}')
        p1_10.plot(x=xValue, y=df[f'{df_list[46]}'], pen=(204, 166, 61), name=f'{df_list[46]}')
        p1_10.plot(x=xValue, y=df[f'{df_list[47]}'], pen=(159, 201, 60), name=f'{df_list[47]}')
        p1_10.plot(x=xValue, y=df[f'{df_list[48]}'], pen=(61, 183, 204), name=f'{df_list[48]}')
        p1_10.plot(x=xValue, y=df[f'{df_list[49]}'], pen=(128, 65, 217), name=f'{df_list[49]}')
        p1_11.plot(x=xValue, y=df[f'{df_list[50]}'], pen=(204, 61, 61), name=f'{df_list[50]}')
        p1_11.plot(x=xValue, y=df[f'{df_list[51]}'], pen=(204,166, 61), name=f'{df_list[51]}')
        p1_11.plot(x=xValue, y=df[f'{df_list[52]}'], pen=(159,201, 60), name=f'{df_list[52]}')
        p1_11.plot(x=xValue, y=df[f'{df_list[53]}'], pen=( 61,183,204), name=f'{df_list[53]}')
        p1_11.plot(x=xValue, y=df[f'{df_list[54]}'], pen=(128, 65,217), name=f'{df_list[54]}')
        p1_12.plot(x=xValue, y=df[f'{df_list[55]}'], pen=(204, 61, 61), name=f'{df_list[55]}')
        p1_12.plot(x=xValue, y=df[f'{df_list[56]}'], pen=(204, 166, 61), name=f'{df_list[56]}')
        p1_12.plot(x=xValue, y=df[f'{df_list[57]}'], pen=(159, 201, 60), name=f'{df_list[57]}')
        p1_12.plot(x=xValue, y=df[f'{df_list[58]}'], pen=( 61, 183, 204), name=f'{df_list[58]}')
        p1_12.plot(x=xValue, y=df[f'{df_list[59]}'], pen=(128, 65, 217), name=f'{df_list[59]}')

        # p2_1.plot(x=buy_index, y=buy_price, pen=None, symbolBrush=(200, 0, 0), symbolPen='w', symbol='t', symbolSize=10, name="진입")  # 마커
        # p2_1.plot(x=sell_index, y=sell_price, pen=None, symbolBrush=(0, 0, 200), symbolPen='w', symbol='t1', symbolSize=10, name="청산")  # 마커

        p2_1.plot(x=xValue, y=df[f'{df_list[60]}'], pen=(204, 61, 61), name=f'{df_list[60]}')
        p2_1.plot(x=xValue, y=df[f'{df_list[61]}'], pen=(204, 166, 61), name=f'{df_list[61]}')
        p2_1.plot(x=xValue, y=df[f'{df_list[62]}'], pen=(159, 201, 60), name=f'{df_list[62]}')
        p2_1.plot(x=xValue, y=df[f'{df_list[63]}'], pen=(61, 183, 204), name=f'{df_list[63]}')
        p2_1.plot(x=xValue, y=df[f'{df_list[64]}'], pen=(128, 65, 217), name=f'{df_list[64]}')
        p2_2.plot(x=xValue, y=df[f'{df_list[65]}'], pen=(204, 61, 61), name=f'{df_list[65]}')
        p2_2.plot(x=xValue, y=df[f'{df_list[66]}'], pen=(204, 166, 61), name=f'{df_list[66]}')
        p2_2.plot(x=xValue, y=df[f'{df_list[67]}'], pen=(159, 201, 60), name=f'{df_list[67]}')
        p2_2.plot(x=xValue, y=df[f'{df_list[68]}'], pen=(61, 183, 204), name=f'{df_list[68]}')
        p2_2.plot(x=xValue, y=df[f'{df_list[69]}'], pen=(128, 65, 217), name=f'{df_list[69]}')
        p2_3.plot(x=xValue, y=df[f'{df_list[70]}'], pen=(204, 61, 61), name=f'{df_list[70]}')
        p2_3.plot(x=xValue, y=df[f'{df_list[71]}'], pen=(204, 166, 61), name=f'{df_list[71]}')
        p2_3.plot(x=xValue, y=df[f'{df_list[72]}'], pen=(159, 201, 60), name=f'{df_list[72]}')
        p2_3.plot(x=xValue, y=df[f'{df_list[73]}'], pen=(61, 183, 204), name=f'{df_list[73]}')
        p2_3.plot(x=xValue, y=df[f'{df_list[74]}'], pen=(128, 65, 217), name=f'{df_list[74]}')
        p2_4.plot(x=xValue, y=df[f'{df_list[75]}'], pen=(204, 61, 61), name=f'{df_list[75]}')
        p2_4.plot(x=xValue, y=df[f'{df_list[76]}'], pen=(204, 166, 61), name=f'{df_list[76]}')
        p2_4.plot(x=xValue, y=df[f'{df_list[77]}'], pen=(159, 201, 60), name=f'{df_list[77]}')
        p2_4.plot(x=xValue, y=df[f'{df_list[78]}'], pen=(61, 183, 204), name=f'{df_list[78]}')
        p2_4.plot(x=xValue, y=df[f'{df_list[79]}'], pen=(128, 65, 217), name=f'{df_list[79]}')
        p2_5.plot(x=xValue, y=df[f'{df_list[80]}'], pen=(204, 61, 61), name=f'{df_list[80]}')
        p2_5.plot(x=xValue, y=df[f'{df_list[81]}'], pen=(204, 166, 61), name=f'{df_list[81]}')
        p2_5.plot(x=xValue, y=df[f'{df_list[82]}'], pen=(159, 201, 60), name=f'{df_list[82]}')
        p2_5.plot(x=xValue, y=df[f'{df_list[83]}'], pen=(61, 183, 204), name=f'{df_list[83]}')
        p2_5.plot(x=xValue, y=df[f'{df_list[84]}'], pen=(128, 65, 217), name=f'{df_list[84]}')
        p2_6.plot(x=xValue, y=df[f'{df_list[85]}'], pen=(204, 61, 61), name=f'{df_list[85]}')
        p2_6.plot(x=xValue, y=df[f'{df_list[86]}'], pen=(204, 166, 61), name=f'{df_list[86]}')
        p2_6.plot(x=xValue, y=df[f'{df_list[87]}'], pen=(159, 201, 60), name=f'{df_list[87]}')
        p2_6.plot(x=xValue, y=df[f'{df_list[88]}'], pen=(61, 183, 204), name=f'{df_list[88]}')
        p2_6.plot(x=xValue, y=df[f'{df_list[89]}'], pen=(128, 65, 217), name=f'{df_list[89]}')
        p2_7.plot(x=xValue, y=df[f'{df_list[90]}'], pen=(204, 61, 61), name=f'{df_list[90]}')
        p2_7.plot(x=xValue, y=df[f'{df_list[91]}'], pen=(204, 166, 61), name=f'{df_list[91]}')
        p2_7.plot(x=xValue, y=df[f'{df_list[92]}'], pen=(159, 201, 60), name=f'{df_list[92]}')
        p2_7.plot(x=xValue, y=df[f'{df_list[93]}'], pen=(61, 183, 204), name=f'{df_list[93]}')
        p2_7.plot(x=xValue, y=df[f'{df_list[94]}'], pen=(128, 65, 217), name=f'{df_list[94]}')
        p2_8.plot(x=xValue, y=df[f'{df_list[95]}'], pen=(204, 61, 61), name=f'{df_list[95]}')
        p2_8.plot(x=xValue, y=df[f'{df_list[96]}'], pen=(204, 166, 61), name=f'{df_list[96]}')
        p2_8.plot(x=xValue, y=df[f'{df_list[97]}'], pen=(159, 201, 60), name=f'{df_list[97]}')
        p2_8.plot(x=xValue, y=df[f'{df_list[98]}'], pen=(61, 183, 204), name=f'{df_list[98]}')
        p2_8.plot(x=xValue, y=df[f'{df_list[99]}'], pen=(128, 65, 217), name=f'{df_list[99]}')
        p2_9.plot(x=xValue, y=df[f'{df_list[100]}'], pen=(204, 61, 61), name=f'{df_list[100]}')
        p2_9.plot(x=xValue, y=df[f'{df_list[101]}'], pen=(204, 166, 61), name=f'{df_list[101]}')
        p2_9.plot(x=xValue, y=df[f'{df_list[102]}'], pen=(159, 201, 60), name=f'{df_list[102]}')
        p2_9.plot(x=xValue, y=df[f'{df_list[103]}'], pen=(61, 183, 204), name=f'{df_list[103]}')
        p2_9.plot(x=xValue, y=df[f'{df_list[104]}'], pen=(128, 65, 217), name=f'{df_list[104]}')
        p2_10.plot(x=xValue, y=df[f'{df_list[105]}'], pen=(204, 61, 61), name=f'{df_list[105]}')
        p2_10.plot(x=xValue, y=df[f'{df_list[106]}'], pen=(204, 166, 61), name=f'{df_list[106]}')
        p2_10.plot(x=xValue, y=df[f'{df_list[107]}'], pen=(159, 201, 60), name=f'{df_list[107]}')
        p2_10.plot(x=xValue, y=df[f'{df_list[108]}'], pen=(61, 183, 204), name=f'{df_list[108]}')
        p2_10.plot(x=xValue, y=df[f'{df_list[109]}'], pen=(128, 65, 217), name=f'{df_list[109]}')
        p2_11.plot(x=xValue, y=df[f'{df_list[110]}'], pen=(204, 61, 61), name=f'{df_list[110]}')
        p2_11.plot(x=xValue, y=df[f'{df_list[111]}'], pen=(204, 166, 61), name=f'{df_list[111]}')
        p2_11.plot(x=xValue, y=df[f'{df_list[112]}'], pen=(159, 201, 60), name=f'{df_list[112]}')
        p2_11.plot(x=xValue, y=df[f'{df_list[113]}'], pen=(61, 183, 204), name=f'{df_list[113]}')
        p2_11.plot(x=xValue, y=df[f'{df_list[114]}'], pen=(128, 65, 217), name=f'{df_list[114]}')
        p2_12.plot(x=xValue, y=df[f'{df_list[115]}'], pen=(204, 61, 61), name=f'{df_list[115]}')
        p2_12.plot(x=xValue, y=df[f'{df_list[116]}'], pen=(204, 166, 61), name=f'{df_list[116]}')
        p2_12.plot(x=xValue, y=df[f'{df_list[117]}'], pen=(159, 201, 60), name=f'{df_list[117]}')
        p2_12.plot(x=xValue, y=df[f'{df_list[118]}'], pen=(61, 183, 204), name=f'{df_list[118]}')
        p2_12.plot(x=xValue, y=df[f'{df_list[119]}'], pen=(128, 65, 217), name=f'{df_list[119]}')

        crosshair.crosshair1(main_pg=p1_1, sub_pg1=p1_2, sub_pg2=p1_3,sub_pg3=p1_4,sub_pg4=p1_5,sub_pg5=p1_6,sub_pg6=p1_7,sub_pg7=p1_8,sub_pg8=p1_9,sub_pg9=p1_10,sub_pg10=p1_11,sub_pg11=p1_12)
        crosshair.crosshair2(main_pg=p2_1, sub_pg1=p2_2, sub_pg2=p2_3,sub_pg3=p2_4,sub_pg4=p2_5,sub_pg5=p2_6,sub_pg6=p2_7,sub_pg7=p2_8,sub_pg8=p2_9,sub_pg9=p2_10,sub_pg10=p2_11,sub_pg11=p2_12)

if __name__ == '__main__':
    path = "D:/tele_bot/"
    db_file = "D:/db_files/data.db"
    KRX_file = 'D:/db_files/KRX.db'
    US_file = 'D:/db_files/US.db'
    save_file = "D:/db_files/save.db"

    # start = '20180101'
    # end = '20220101'
    end = 'now'

    delay = 20000 #차멍 딜레이시간 ms(밀리세컨)
    #
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
