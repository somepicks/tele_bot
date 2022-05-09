import sqlite3
import pandas as pd
# pd.set_option('display.max_row',None) #모든 행을 보고자 할 때
pd.set_option('display.max_columns',None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width',1200)
pd.set_option("display.unicode.east_asian_width", True)
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import QFont, QColor,QColor,QPainter, QPicture
from pyqtgraph.dockarea import *
from collections import Counter
from PyQt5 import QtWidgets
from pandas import Series
pd.set_option('mode.chained_assignment',  None) # SettingWithCopyWarning 경고를 끈다
import sys
import os.path
import math
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,QTabWidget
from PyQt5.QtTest import *
import pyupbit
import make_indicator
from PyQt5.QtCore import QRectF, QPointF
def stock_infomation(stock_id):
    stock_list = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    stock_list.종목코드 = stock_list.종목코드.map('{:06d}'.format)

    #우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
    stock_list = stock_list[['회사명', '종목코드','업종','주요제품','상장일']]

    stock_code = make_stock_code(stock_id,stock_list)
    stock_name = make_stock_name(stock_id,stock_list)
    stock_info = stock_list.loc[stock_list['회사명'] == stock_name]
    # print(stock_info)

    return stock_code,stock_name,stock_info
def make_stock_code(id,stock_list):
    # print(id.isalpha()) #stock_id가 문자열인지 확인
    if id.isalpha() == True: #stock_id가 문자열일 경우
        stock_info = stock_list.loc[stock_list['회사명']==id]
        code = stock_info.iloc[0]['종목코드'] #종목코드로 변환
        return code
    elif id.isalpha() == False:
        code = id
        return code
def make_stock_name(id,stock_list):
    if id.isdigit() == True:
        stock_info = stock_list.loc[stock_list['종목코드']==id]
        name = stock_info.iloc[0]['회사명'] #회사명으로 변환
        return name
    elif id.isdigit() == False:
        name = id
        return name
def df_date(df,date):
    date = date.replace('/', '')  # date변수의 '/'를 제거 후 저장
    date = date.replace('~', '')  # date변수의 '~'를 제거 후 저장
    df.index = df.index.astype(str)
    try:
        df.loc[df.index,'날짜'] = df.index.str[4:8] ##index에서 str짤라가지고 date컬럼 생성
        # df['날짜'] = df.index.str[4:8] #index에서 str짤라가지고 date컬럼 생성
    except:
        print('* 백테스트 DB파일 중복 *')
        quit()
    if len(date) == 4: # 날짜변수로 4글자가 오면
        if (df['날짜']==date).any(): #'날짜'컬럼에 date가 포함되는지 여부, all() 사용 시 -모든값이 date인지
            df = df[df.날짜 == date]  # date변수와 일치하는 'date'컬럼 값 만 df에 저장
        else:
            df = pd.DataFrame().copy()
            print('* 일치하는 날짜 없음 *')
            # quit()
        # print('date =', date[0][:2],"/",date[0][2:])
    elif len(date) == 8: # 날짜변수로 8글자가 오면
        # groups = df.groupby('날짜') #날짜별 그룹 만들기
        # print(groups.size())
        df = df[df.날짜 >= date[0:4]] #date변수의 앞숫자 보다 크거나 같은 값의 범위만 df에 저장
        df = df[df.날짜 <= date[4:8]] #date변수의 뒷숫자 보다 작거나 같은 값의 범위만 df에 다시 저장
    elif date == 'all' or date == 'ALL':
        print('모든 날짜 보기')
    else:
        print('* date값 확인 필요 *')
        df=pd.DataFrame().copy()
    return df
def df_time(df,start,end):
    start = start.replace(':', '')  # date변수의 ':'를 제거 후 저장
    end = end.replace(':', '')  # date변수의 ':'를 제거 후 저장
    start = start+'00' #시작시간에 초 를 더하기
    start = int(start) #시작시간을 정수형으로 변환
    end = end+'00' #끝시간에 초 를 더하기
    end = int(end) #끝시간을 정수형으로 변환

    df['시간'] = df.index.str[8:14]  ##index에서 str짤라가지고 '시간'컬럼 생성
    df = df.astype({'시간':'int'}) #'시간'컬럼을 int형으로 변환
    df = df[df.시간 >= start] #'시간'컴럼의 값이 start보다 큰 값만 저장
    df = df[df.시간 <= end] #'시간'컴럼의 값이 end보다 작은 값만 저장
    return df
def df_backtest(stock_name,df,date,start,end,back_file):
    if not os.path.isfile(back_file):
        print('* 백테스트 db파일 없음 - 경로 확인 *')
        quit()
    con = sqlite3.connect(back_file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    back_table = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
    # back_table = np.concatenate(back_table).tolist() #모든테이블을 리스트로변환 https://codechacha.com/ko/python-flatten-list/
    # print(back_table)
    # print('불러올 백테스트 테이블:',back_table[-1])
    if not back_table:
        print('* 백테스트 db파일이 비어있음 *')
        quit()
    back_time=back_table[-1]
    back_time=str(back_time)[1:-2]
    df_back_list = pd.read_sql("SELECT * FROM " + back_time, con).set_index('index')
    con.close()
    # cursor.close()
    df_back_list = df_date(df_back_list,date) #백테스트 날짜 슬라이싱
    df_back_list = df_time(df_back_list,start,end) #백테스트 시간 슬라이싱
    # print(df_back_list)
    if df_back_list.empty: #빈 데이터 프레임일 경우
        print('* 조회 날짜 또는 시간 조절 필요 *')
        quit()
    def back_list_sort(df_back_list): # 동일시간 매수 또는 매도 시 겹치는 행이 있어서 컬럼마다 풀어주기 위함
        stock_name = df_back_list['종목명'].str.split(';').apply(Series, 1).stack() #겹친 '종목명'을 개별로 풀어줌
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
        del df_back_list['날짜']
        del df_back_list['시간']
        del df_back_list['수익금']
        del df_back_list['수익금합계']
        df_back_list = pd.concat([stock_name, buy_time, sell_time, buy_price, sell_price, profit],
                                 axis=1)  # 시리즈를 열방향으로 합치기
        df_back_list.reset_index(drop=False, inplace=True)  # index를 순번으로 리셋
        del df_back_list['index']
        return df_back_list
    df_back_list = back_list_sort(df_back_list)
    # marker_index=df_back_list.index[df_back_list['종목명'].str.contains(stock_name)].tolist() #종목명 매칭하여 하나라도 동일한 글자가 들어가면 인덱스 값 추출
    marker_index=df_back_list.index[df_back_list['종목명'] == stock_name].tolist() #종목명 매칭하여 완벽히 동일한 글자가 들어가면 인덱스 값 추출
    # print(marker_index)
    if not marker_index :
        print('* 백테스트 db파일에 종목 없음 *')
        quit()
    df_back = df_back_list.loc[marker_index] #인덱스 매칭하여 해당 행 만추출
    df_back_time_buy = df_back[['매수시간','매수가']] #매수에 대한 DF추출
    df_back_time_sell = df_back[['매도시간','매도가','수익률']]#매도에 대한 DF추출
    df_back_time_buy.set_index('매수시간',inplace=True) #매수에 대한 인덱스 재 정의
    df_back_time_sell.set_index('매도시간',inplace=True) #매도에 대한 인덱스 재 정의
    df_back_time_buy = df_back_time_buy.astype(float) #str을 float으로 변환
    df_back_time_sell = df_back_time_sell.astype(float)
    df_back = pd.concat([df_back_time_buy,df_back_time_sell]) # buy + sell 행방향으로 합치기
    df.drop(['매수가','매도가'],axis=1,inplace=True)
    df=pd.merge(df, df_back,left_index = True, right_index = True,how = 'left') # df + df_back 합치기
    #백테스트에 포함되는 날짜만 남기고 나머지 df는 삭제 (여러날짜를 한번에 조회할 때 사용)
    date_back = df_back_time_buy.index.str[4:8].tolist() #인덱스를 짤라서 리스트로 변환
    date_back=list(set(date_back)) #리스트 중복 제거
    groups = df.groupby('날짜')  # 날짜별 그룹 만들기
    groups_date = groups.size().index.tolist() #날짜별 그룹의 인덱스(날짜)를 리스트로 저장
    un_date_back=list(set(groups_date) - set(date_back)) # df날짜에서 백테스트 날짜의 차집합

    for un_date in un_date_back:
        df.drop(df.loc[df['날짜'] == un_date].index, inplace=True) #백테스트db에 없는 날짜는 삭제
    return df

def crosshair1(main_pg, sub_pg1, sub_pg2,sub_pg3,sub_pg4,sub_pg5,sub_pg6,sub_pg7,sub_pg8,sub_pg9,sub_pg10,sub_pg11):
    vLine1 = pg.InfiniteLine()
    vLine1.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine2 = pg.InfiniteLine()
    vLine2.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine3 = pg.InfiniteLine()
    vLine3.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine4 = pg.InfiniteLine()
    vLine4.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine5 = pg.InfiniteLine()
    vLine5.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine6 = pg.InfiniteLine()
    vLine6.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine7 = pg.InfiniteLine()
    vLine7.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine8 = pg.InfiniteLine()
    vLine8.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine9 = pg.InfiniteLine()
    vLine9.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine10 = pg.InfiniteLine()
    vLine10.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine11 = pg.InfiniteLine()
    vLine11.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine12 = pg.InfiniteLine()
    vLine12.setPen(pg.mkPen(QColor(230, 230, 0), width=1))

    # hLine1 = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k', width=1), label='{value:0.1f}',
    #                                     labelOpts={'position':0.1, 'color': (200,0,0), 'movable': True, 'fill': (0, 0, 200, 100)})
    hLine1 = pg.InfiniteLine(angle=0)
    hLine1.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine2 = pg.InfiniteLine(angle=0)
    hLine2.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine3 = pg.InfiniteLine(angle=0)
    hLine3.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine4 = pg.InfiniteLine(angle=0)
    hLine4.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine5 = pg.InfiniteLine(angle=0)
    hLine5.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine6 = pg.InfiniteLine(angle=0)
    hLine6.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine7 = pg.InfiniteLine(angle=0)
    hLine7.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine8 = pg.InfiniteLine(angle=0)
    hLine8.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine9 = pg.InfiniteLine(angle=0)
    hLine9.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine10 = pg.InfiniteLine(angle=0)
    hLine10.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine11 = pg.InfiniteLine(angle=0)
    hLine11.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine12 = pg.InfiniteLine(angle=0)
    hLine12.setPen(pg.mkPen(QColor(230, 230, 0), width=1))


    main_pg.addItem(vLine1, ignoreBounds=True)
    main_pg.addItem(hLine1, ignoreBounds=True)
    sub_pg1.addItem(vLine2, ignoreBounds=True)
    sub_pg1.addItem(hLine2, ignoreBounds=True)
    sub_pg2.addItem(vLine3, ignoreBounds=True)
    sub_pg2.addItem(hLine3, ignoreBounds=True)
    sub_pg3.addItem(vLine4, ignoreBounds=True)
    sub_pg3.addItem(hLine4, ignoreBounds=True)
    sub_pg4.addItem(vLine5, ignoreBounds=True)
    sub_pg4.addItem(hLine5, ignoreBounds=True)
    sub_pg5.addItem(vLine6, ignoreBounds=True)
    sub_pg5.addItem(hLine6, ignoreBounds=True)
    sub_pg6.addItem(vLine7, ignoreBounds=True)
    sub_pg6.addItem(hLine7, ignoreBounds=True)
    sub_pg7.addItem(vLine8, ignoreBounds=True)
    sub_pg7.addItem(hLine8, ignoreBounds=True)
    sub_pg8.addItem(vLine9, ignoreBounds=True)
    sub_pg8.addItem(hLine9, ignoreBounds=True)
    sub_pg9.addItem(vLine10, ignoreBounds=True)
    sub_pg9.addItem(hLine10, ignoreBounds=True)
    sub_pg10.addItem(vLine11, ignoreBounds=True)
    sub_pg10.addItem(hLine11, ignoreBounds=True)
    sub_pg11.addItem(vLine12, ignoreBounds=True)
    sub_pg11.addItem(hLine12, ignoreBounds=True)

    main_vb = main_pg.getViewBox()
    sub_vb1 = sub_pg1.getViewBox()
    sub_vb2 = sub_pg2.getViewBox()
    sub_vb3 = sub_pg3.getViewBox()
    sub_vb4 = sub_pg4.getViewBox()
    sub_vb5 = sub_pg5.getViewBox()
    sub_vb6 = sub_pg6.getViewBox()
    sub_vb7 = sub_pg7.getViewBox()
    sub_vb8 = sub_pg8.getViewBox()
    sub_vb9 = sub_pg9.getViewBox()
    sub_vb10 = sub_pg10.getViewBox()
    sub_vb11 = sub_pg11.getViewBox()


    def mouseMoved(evt):
        pos = evt[0]
        if main_pg.sceneBoundingRect().contains(pos):
            mousePoint = main_vb.mapSceneToView(pos)
            # self.ct_labellll_03.setText(f"현재가 {format(round(mousePoint.y(), 2), ',')}")
            hLine1.setPos(mousePoint.y())#주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg1.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb1.mapSceneToView(pos)
            # self.ct_labellll_04.setText(f"체결강도 {format(round(mousePoint.y(), 2), ',')}")
            hLine2.setPos(mousePoint.y())#주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg2.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb2.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine3.setPos(mousePoint.y())#주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg3.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb3.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine4.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg4.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb4.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine5.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg5.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb5.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine6.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg6.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb6.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine7.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg7.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb7.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine8.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg8.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb8.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine9.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg9.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb9.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine10.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg10.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb10.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine11.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg11.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb11.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine12.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())

    main_pg.proxy = pg.SignalProxy(main_pg.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg1.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg2.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg3.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg4.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg5.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg6.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg7.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg8.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg9.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg11.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg10.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
def crosshair2(main_pg, sub_pg1, sub_pg2,sub_pg3,sub_pg4,sub_pg5,sub_pg6,sub_pg7,sub_pg8,sub_pg9,sub_pg10,sub_pg11):
    vLine1 = pg.InfiniteLine()
    vLine1.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine2 = pg.InfiniteLine()
    vLine2.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine3 = pg.InfiniteLine()
    vLine3.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine4 = pg.InfiniteLine()
    vLine4.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine5 = pg.InfiniteLine()
    vLine5.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine6 = pg.InfiniteLine()
    vLine6.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine7 = pg.InfiniteLine()
    vLine7.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine8 = pg.InfiniteLine()
    vLine8.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine9 = pg.InfiniteLine()
    vLine9.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine10 = pg.InfiniteLine()
    vLine10.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine11 = pg.InfiniteLine()
    vLine11.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    vLine12 = pg.InfiniteLine()
    vLine12.setPen(pg.mkPen(QColor(230, 230, 0), width=1))

    # hLine1 = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k', width=1), label='{value:0.1f}',
    #                                     labelOpts={'position':0.1, 'color': (200,0,0), 'movable': True, 'fill': (0, 0, 200, 100)})
    hLine1 = pg.InfiniteLine(angle=0)
    hLine1.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine2 = pg.InfiniteLine(angle=0)
    hLine2.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine3 = pg.InfiniteLine(angle=0)
    hLine3.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine4 = pg.InfiniteLine(angle=0)
    hLine4.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine5 = pg.InfiniteLine(angle=0)
    hLine5.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine6 = pg.InfiniteLine(angle=0)
    hLine6.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine7 = pg.InfiniteLine(angle=0)
    hLine7.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine8 = pg.InfiniteLine(angle=0)
    hLine8.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine9 = pg.InfiniteLine(angle=0)
    hLine9.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine10 = pg.InfiniteLine(angle=0)
    hLine10.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine11 = pg.InfiniteLine(angle=0)
    hLine11.setPen(pg.mkPen(QColor(230, 230, 0), width=1))
    hLine12 = pg.InfiniteLine(angle=0)
    hLine12.setPen(pg.mkPen(QColor(230, 230, 0), width=1))


    main_pg.addItem(vLine1, ignoreBounds=True)
    main_pg.addItem(hLine1, ignoreBounds=True)
    sub_pg1.addItem(vLine2, ignoreBounds=True)
    sub_pg1.addItem(hLine2, ignoreBounds=True)
    sub_pg2.addItem(vLine3, ignoreBounds=True)
    sub_pg2.addItem(hLine3, ignoreBounds=True)
    sub_pg3.addItem(vLine4, ignoreBounds=True)
    sub_pg3.addItem(hLine4, ignoreBounds=True)
    sub_pg4.addItem(vLine5, ignoreBounds=True)
    sub_pg4.addItem(hLine5, ignoreBounds=True)
    sub_pg5.addItem(vLine6, ignoreBounds=True)
    sub_pg5.addItem(hLine6, ignoreBounds=True)
    sub_pg6.addItem(vLine7, ignoreBounds=True)
    sub_pg6.addItem(hLine7, ignoreBounds=True)
    sub_pg7.addItem(vLine8, ignoreBounds=True)
    sub_pg7.addItem(hLine8, ignoreBounds=True)
    sub_pg8.addItem(vLine9, ignoreBounds=True)
    sub_pg8.addItem(hLine9, ignoreBounds=True)
    sub_pg9.addItem(vLine10, ignoreBounds=True)
    sub_pg9.addItem(hLine10, ignoreBounds=True)
    sub_pg10.addItem(vLine11, ignoreBounds=True)
    sub_pg10.addItem(hLine11, ignoreBounds=True)
    sub_pg11.addItem(vLine12, ignoreBounds=True)
    sub_pg11.addItem(hLine12, ignoreBounds=True)

    main_vb = main_pg.getViewBox()
    sub_vb1 = sub_pg1.getViewBox()
    sub_vb2 = sub_pg2.getViewBox()
    sub_vb3 = sub_pg3.getViewBox()
    sub_vb4 = sub_pg4.getViewBox()
    sub_vb5 = sub_pg5.getViewBox()
    sub_vb6 = sub_pg6.getViewBox()
    sub_vb7 = sub_pg7.getViewBox()
    sub_vb8 = sub_pg8.getViewBox()
    sub_vb9 = sub_pg9.getViewBox()
    sub_vb10 = sub_pg10.getViewBox()
    sub_vb11 = sub_pg11.getViewBox()


    def mouseMoved(evt):
        pos = evt[0]
        if main_pg.sceneBoundingRect().contains(pos):
            mousePoint = main_vb.mapSceneToView(pos)
            # self.ct_labellll_03.setText(f"현재가 {format(round(mousePoint.y(), 2), ',')}")
            hLine1.setPos(mousePoint.y())#주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg1.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb1.mapSceneToView(pos)
            # self.ct_labellll_04.setText(f"체결강도 {format(round(mousePoint.y(), 2), ',')}")
            hLine2.setPos(mousePoint.y())#주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg2.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb2.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine3.setPos(mousePoint.y())#주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg3.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb3.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine4.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg4.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb4.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine5.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg5.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb5.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine6.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg6.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb6.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine7.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg7.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb7.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine8.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg8.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb8.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine9.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg9.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb9.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine10.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg10.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb10.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine11.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())
        elif sub_pg11.sceneBoundingRect().contains(pos):
            mousePoint = sub_vb11.mapSceneToView(pos)
            # self.ct_labellll_05.setText(f"초당거래대금 {format(round(mousePoint.y(), 2), ',')}")
            hLine12.setPos(mousePoint.y()) #주석처리하면 세로만 나옴
            vLine1.setPos(mousePoint.x())
            vLine2.setPos(mousePoint.x())
            vLine3.setPos(mousePoint.x())
            vLine4.setPos(mousePoint.x())
            vLine5.setPos(mousePoint.x())
            vLine6.setPos(mousePoint.x())
            vLine7.setPos(mousePoint.x())
            vLine8.setPos(mousePoint.x())
            vLine9.setPos(mousePoint.x())
            vLine10.setPos(mousePoint.x())
            vLine11.setPos(mousePoint.x())
            vLine12.setPos(mousePoint.x())

    main_pg.proxy = pg.SignalProxy(main_pg.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg1.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg2.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg3.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg4.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg5.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg6.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg7.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg8.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg9.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg11.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
    sub_pg10.proxy = pg.SignalProxy(sub_pg1.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)

def get_data(stock_code,date,start,end,stock_file):
    if not os.path.isfile(stock_file):
        print('* 파일 없음 - 경로 확인 *')
        quit()
    con = sqlite3.connect(stock_file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = cursor.fetchall() #fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
    table_list = np.concatenate(table_list).tolist() #모든테이블을 리스트로변환 https://codechacha.com/ko/python-flatten-list/
    try:
        df = pd.read_sql("SELECT * FROM " + "'" + stock_code + "'", con).set_index('index')
    except:
        print('* db파일에 종목 없음 *')
        df = []
        quit()

    df = df_date(df, date)
    df = df_time(df, start, end)
    if df.empty:
        print('* db테이블에 종목은 있으나 데이터가 비어있음 - 확인 필요 *')
        quit()

    con.close()
    return df,table_list

class Window(QWidget): #pyqtGraph를 Qwidget에 담기
    def __init__(self,df,stock_name):
        super().__init__()
        # self.win = pg.GraphicsLayoutWidget(show=True)
        self.win1 = pg.GraphicsLayoutWidget(self) #pyqtgraph
        self.win2 = pg.GraphicsLayoutWidget(self) #pyqtgraph
        # self.win2 = pg.GraphicsLayoutWidget(self) #pyqtgraph

        tabs = QTabWidget()
        tabs.addTab(self.win1, 'Tab1')
        tabs.addTab(self.win2, 'Tab2')
        # self.win.setWindowTitle('주식차트')
        # self.win.setGeometry(0, 0, 3850, 1010)
        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)
        vbox.setContentsMargins(0,0,0,0)
        self.win1.setGeometry(0, 0, 3850, 1010)
        self.win2.setGeometry(0, 0, 3850, 1010)
        # self.win.setMaximumWidth(500)
        # self.win.setMaximumHeight(500)

        bottomAxis = pg.AxisItem(orientation='bottom')
        # bottomAxis_date = pg.AxisItem(orientation='bottom')
        # print(bottomAxis)
        # quit()
        # link_view
        area = DockArea()
        # d1 = Dock("Dock1")
        area.addDock(Dock("Dock1"), 'bottom')
        #
        # p1 = self.win.addPlot(row=0, col=0,title=stock_name + date,axisItems={'bottom': pg.DateAxisItem()})
        # p2 = self.win.addPlot(row=1, col=0,title='체결강도',axisItems={'bottom': pg.AxisItem(orientation='bottom')})

        p1_1  = self.win1.addPlot(row=0, col=0,title=f'{stock_name}',axisItems={'bottom': pg.DateAxisItem()})
        p1_2  = self.win1.addPlot(row=1, col=0,title='체결강도',axisItems={'bottom': pg.DateAxisItem()})
        p1_3  = self.win1.addPlot(row=2, col=0,title='체결강도/등락율',axisItems={'bottom': pg.DateAxisItem()})
        p1_4  = self.win1.addPlot(row=0, col=1,title='거래대금',axisItems={'bottom': pg.DateAxisItem()})
        p1_5  = self.win1.addPlot(row=1, col=1,title='거래대금/속도',axisItems={'bottom': pg.DateAxisItem()})
        p1_6  = self.win1.addPlot(row=2, col=1,title='거래대금평균',axisItems={'bottom': pg.DateAxisItem()})
        p1_7  = self.win1.addPlot(row=0, col=2,title='초당대금',axisItems={'bottom': pg.DateAxisItem()})
        p1_8  = self.win1.addPlot(row=1, col=2,title='초당대금평균',axisItems={'bottom': pg.DateAxisItem()})
        p1_9  = self.win1.addPlot(row=2, col=2,title='총잔량',axisItems={'bottom': pg.DateAxisItem()})
        p1_10 = self.win1.addPlot(row=0, col=3,title='호가',axisItems={'bottom': pg.DateAxisItem()})
        p1_11 = self.win1.addPlot(row=1, col=3,title='잔량1',axisItems={'bottom': pg.DateAxisItem()})
        p1_12 = self.win1.addPlot(row=2, col=3,title='잔량2',axisItems={'bottom': pg.DateAxisItem()})


        p2_1  = self.win2.addPlot(row=0, col=0, title=f'{stock_name}',axisItems={'bottom': pg.DateAxisItem()})
        p2_2  = self.win2.addPlot(row=1, col=0, title='체결강도', axisItems={'bottom': pg.DateAxisItem()})
        p2_3  = self.win2.addPlot(row=2, col=0, title='체결강도', axisItems={'bottom': pg.DateAxisItem()})
        p2_4  = self.win2.addPlot(row=0, col=1, title='거래대금', axisItems={'bottom': pg.DateAxisItem()})
        p2_5  = self.win2.addPlot(row=1, col=1, title='등락율',   axisItems={'bottom': pg.DateAxisItem()})
        p2_6  = self.win2.addPlot(row=2, col=1, title='고저평균대비등락율', axisItems={'bottom': pg.DateAxisItem()})
        p2_7  = self.win2.addPlot(row=0, col=2, title='초당대금', axisItems={'bottom': pg.DateAxisItem()})
        p2_8  = self.win2.addPlot(row=1, col=2, title='초당대금평균', axisItems={'bottom': pg.DateAxisItem()})
        p2_9  = self.win2.addPlot(row=2, col=2, title='총잔량', axisItems={'bottom': pg.DateAxisItem()})
        p2_10 = self.win2.addPlot(row=0, col=3, title='호가', axisItems={'bottom': pg.DateAxisItem()})
        p2_11 = self.win2.addPlot(row=1, col=3, title='잔량1', axisItems={'bottom': pg.DateAxisItem()})
        p2_12 = self.win2.addPlot(row=2, col=3, title='잔량2', axisItems={'bottom': pg.DateAxisItem()})

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

        # df['index_time'] = pd.to_datetime(df.index, format='%Y%m%d%H%M%S').astype(str) #index시간컬럼을 str타입의 datetime형식으로 생성
        # df=df.drop_duplicates(['index_time']) #시간이 중복인 행 제거
        # df.loc[df.index, 'index_time'] = df[df.index_time.str[-2:] == '00']   # index_time의 초가 '00'인 경우만 index_time컬럼 값 저장
        # df['index_time'] = df['index_time'].str[11:-3] #분만 표시하기 위해 초 제거
        # df['index_time'] = df['index_time'].replace(np.nan,'',regex=True) #nan값을 공백으로 변경
        #
        # df['index_date'] = pd.to_datetime(df.index, format='%Y%m%d%H%M%S').astype(str)
        # p = df.index[df['날짜']!=df['날짜'].shift(1)] # 날짜가 바뀌는 행의 인덱스를 추출
        # df['index_date'] = df.loc[p,'index_date'] #추출한 인덱스값의 'index_date'컬럼 값만 남김
        # df['index_date'] = df['index_date'].str[5:11]
        # df['index_date'] = df['index_date'].replace(np.nan,'',regex=True) #nan값을 공백으로 변경
        #
        # df['index_chart']=df['index_date']+df['index_time'] #더하기
        # df['index_chart'] = df['index_chart'].str[0:5]
        # # df['index_chart'] = df['index_chart'].replace(end,'',regex=True) #차트의 마지막 index 값을 공백으로 변경
        # time = df['index_chart'].tolist()
        # # df['매수가'] = df['매수가'].replace(np.nan,'',regex=True) #nan값을 공백으로 변경
        #
        # df['number'] = range(0,len(df)) # 넘버링 컬럼 추가
        # print(df)
        # buy_index = df['number'][df['매수가'].isna() == False] #'매수가'가 nan이 아닌 행의 'number' 컬럼 값을 추출
        # buy_price = df['매수가'][df['매수가'].isna() == False] #'매수가'가 nan이 아닌 행의 '매수가' 컬럼의 값을 추출
        # sell_index = df['number'][df['매도가'].isna() == False] #'매도가'가 nan이 아닌 행의 'number' 컬럼 값을 추출
        # sell_price = df['매도가'][df['매도가'].isna() == False] #'매도가'가 nan이 아닌 행의 '매도가' 컬럼의 값을 추출
        #
        # xDict=dict(enumerate(time))
        # xValue=list(xDict.keys())
        # xtickts=[xDict.items()]
        # bottomAxis.setTicks(xtickts)
        #
        # date = df['index_date'].tolist()
        # xDict=dict(enumerate(date))
        # xDate=list(xDict.keys())
        # xtickts_date=[xDict.items()]
        # bottomAxis_date.setTicks(xtickts_date)

        # print('사용가능지표: ',end="")
        # for i in range (len(df.columns)):
        #     col_name = df.columns[i]
        #     globals()['{}'.format(col_name)] = df[col_name].tolist()
        #     print(col_name,', ',end="")
        #     if i % 16==0:
        #         print('\n')


        # df.index = df.index.astype(np.int64) #index를 df['index_time']컬럼의 datetime64 타입으로 저장 2022-01-05
        df.index=df.index.astype(np.int64)
        # print(df)
        # print(df.index.dtype)
        df.index = pd.to_datetime(df.index, format='%Y%m%d') #index를 df['index_time']컬럼의 datetime64 타입으로 저장 2022-01-05

        # df=df.index.astype('datetime64[ns]')
        print(df)
        x_df = [int(x.timestamp())-32400 for x in df.index]
        # quit()

        y_dot = pg.mkPen(color='y', width=1, style=QtCore.Qt.DotLine)
        g_dot = pg.mkPen(color='g', width=1, style=QtCore.Qt.DotLine)
        r_dash = pg.mkPen(color='r', width=1, style=QtCore.Qt.DashLine)
        g_dash = pg.mkPen(color=[0,130,153], width=1.2, style=QtCore.Qt.DashLine)

        # item1 = CandlestickItem(df)
        # item2 = HeikinItem(df)
        # p1.addItem(item1)

        p1_1.plot(x=x_df, y=df['high'  ], pen=r_dash,       name='high')
        p1_1.plot(x=x_df, y=df['low'  ], pen=r_dash,name='low')
        p1_1.plot(x=x_df, y=df['ma5'], pen=(120,200,200),name='ma5')
        p1_1.plot(x=x_df, y=df['ma60' ], pen=(120,150,150),name='ma60')
        p1_1.plot(x=x_df, y=df['ma60마지' ], pen=y_dot,name='ma60마지')
        p1_1.plot(x=x_df, y=df['ma300' ], pen=(128, 65,217),name='ma300')
        p1_1.plot(x=x_df, y=df['ma300마지' ], pen=g_dot,name='ma300마지')
        p1_1.plot(x=x_df, y=df['ma'], pen=(204,114, 61),name='ma')
        p1_1.plot(x=x_df, y=df['close'], pen=(200, 50, 50),name='close')

        # p1.plot(x=buy_index, y=buy_price,   pen =None, symbolBrush =(200,  0,  0),symbolPen ='w', symbol='t' , symbolSize=10, name="진입") #마커
        # p1.plot(x=sell_index, y=sell_price, pen =None, symbolBrush =(  0,  0,200),symbolPen ='w', symbol='t1', symbolSize=10, name="청산") #마커

        # p2.addItem(item2)
        p1_2.plot(x=x_df, y=df['고저평균대비등락율'],pen=(200, 50, 50),fillLevel=0,brush=(100,50,200,50),name='고저평균대비등락율')
        # p2.plot(x=x_df, y=df['체결강도최고'],pen=y_dot,name='체결강도최고')
        # p2.plot(x=x_df, y=df['체결강도최저'],pen=g_dot,name='체결강도최저')
        # p2.plot(x=x_df, y=df['체결강도평균마지+'], pen=g_dash,name='체결강도평균마지+')
        # p2.plot(x=x_df, y=df['체결강도평균마지-'], pen=g_dash,name='체결강도평균마지-')

        p1_3.plot(x=x_df, y=df['최고등락'], pen=(0, 250, 0),name='최고등락')
        p1_3.plot(x=x_df, y=df['최고등락평균'], pen=(50, 100, 50),name='최고등락평균')
        p1_3.plot(x=x_df, y=df['등락'], pen=(242,203, 95),name='고저평균대비등락율')
        p1_3.plot(x=x_df, y=df['등락평균'], pen=(50, 50, 200),name='등락평균')
        # p3.plot(x=x_df, y=df['체강차체강평균'], pen=(152, 20, 20),name='체강-체강평균')
        # p3.plot(x=x_df, y=df['체강차체강평균최저'], pen=g_dot,name='체강-체강평균(최저)')
        # p3.plot(x=x_df, y=df['체강차체강평균최고'], pen=y_dot,name='체강-체강평균(최고)')

        # p1_4.plot(x=x_df,y=df['거래대금차'], pen='c',fillLevel=3000,fillOutline=True, brush=(50,50,200,50),skipFiniteCheck= False,name='거래대금차')
        # p1_4.plot(x=x_df, y=df['거래대금차평균'],     pen=(200, 50, 50),name='거래대금차평균')

        # p5.plot(x=x_df, y=df['초당거래대금'], pen=(50, 50, 200),name='초당거래대금')
        # p5.plot(x=x_df, y=df['초당거래대금변동'], pen=(50, 50, 200),name='초당거래대금변동')
        # p5.plot(x=x_df, y=df['직전초당거래대금'], pen=y_dot,name='초당거래대금평균최고')
        # p1_5.plot(x=x_df, y=df['거래대금변동'], pen=g_dot,name='거래대금변동')
        # p1_5.plot(x=x_df, y=df['거래대금변동절대'],     pen=(120,200,200),name='거래대금변동절대')
        # p1_5.plot(x=x_df, y=df['거래대금변동평균' ],pen=(0, 250, 0),name='거래대금변동평균')
        # p1_5.plot(x=x_df, y=df['거래대금평균최고' ],pen=(200, 50, 50),name='거래대금평균최고')
        # p1_5.plot(x=x_df, y=df['거래대금평균최고마지' ],pen=(128, 65,217),name='거래대금평균최고마지')
        # p1_5.plot(x=x_df, y=df['초대금평균차초대금평균최고' ],pen=(50, 50, 200),name='초대금평균차초대금평균최고')


        # p1_6.plot(x=x_df, y=df['거래대금평균60' ],  pen=(120,200,200), name='거래대금평균60')
        # p1_6.plot(x=x_df, y=df['거래대금평균120'],  pen=(128, 65,217), name='거래대금평균120')

        p1_7.plot(x=x_df, y=df['수익률'  ], pen=(200, 50, 50),name=  '수익률')
        # p1_7.plot(x=x_df, y=df['renko6평균'   ], pen=(204,114, 61),name= 'renko6평균')
        # p1_7.plot(x=x_df, y=df['renko9평균'  ], pen=(120,200,200),name=  'renko9평균')
        # p1_7.plot(x=x_df, y=df['renko_bricks' ], pen=(120,150,150),name= 'namerenko_bricks')
        # p7.plot(x=x_df, y=df['거래대금각도'],     pen=(152, 20, 20),name='거래대금각도')
        # p7.plot(x=x_df, y=df['초당매도수량'],     pen=(20 , 50,150),name='초당매도수량')

        # p1_8.plot(x=x_df, y=df['봉거래대금'], pen=(200, 50, 50),name='봉거래대금')
        # p1_8.plot(x=x_df, y=df['봉거래대금평균'], pen=y_dot,name='봉거래대금평균')
        # p1_8.plot(x=x_df, y=df['봉거래대금평균최고'], pen=(120,200,200),name='봉거래대금평균최고')
        # p8.plot(x=xValue, y=df['초당거래대금평균'],     pen=(100, 50, 50),name='초당거래대금평균')
        #
        p1_9.plot(x=x_df, y=df['Volume'],pen=('w'),name='Volume')
        # p9.plot(x=xDate, y=df['매수총잔량평균'], pen=(200, 50, 50),fillLevel=7000,brush=(100,50,200,50),name='매수총잔량평균')
        # p9.plot(x=xDate, y=df['매도총잔량평균'], pen=(120,200,200),name='매도총잔량평균')
        # p9.plot(x=xDate, y=df['매수총잔량평균최저'], pen=y_dot,name='매수총잔량평균최저')
        # p9.plot(x=xDate, y=df['매도총잔량평균최고'], pen=y_dot,name='매도총잔량평균최고')
        # p9.plot(x=xDate, y=df['매도총잔량평균최저'], pen=g_dot,name='매도총잔량평균최저')


        # p1_10.plot(x=x_df, y=df['value'], pen=(255,  0,  0),name='value')
        # p10.plot(x=xValue, y=df['매수호가2'], pen=(255, 94,  0),name='매수호가2')
        # p10.plot(x=xValue, y=df['매도호가1'], pen=(  1,  0,255),name='매도호가1')
        # p10.plot(x=xValue, y=df['매도호가2'], pen=( 95,  0,255),name='매도호가2')
        # p10.plot(x=xValue, y=df['초당거래대금']*df['초당매수수량'], pen=(255,  0,  0),name='초당곱')
        # p10.plot(x=xValue, y=(df['초당매수수량']+df['초당매도수량'])*70, pen=(95, 0,  255),name='초당+')
        #
        # p1_11.plot(x=x_df, y=df['hei_open'], pen=r_dash,name='hei_open')
        # p1_11.plot(x=x_df, y=df['hei_close'], pen=(220, 50, 150),name='hei_close')
        # p11.plot(x=x_df, y=df['매수잔량1평균'], pen=(242, 203, 95), name='매수잔량1평균')
        # p11.plot(x=x_df, y=df['매도잔량1평균'], pen=(92, 210, 229), name='매도잔량1평균')
        # p11.plot(x=x_df, y=df['매도잔량1평균최고'], pen=(y_dot), name='매도잔량1평균최고')
        #
        # p1_12.plot(x=x_df, y=df['renko1_3평균'], pen=(152, 20,  20),name='renko3')
        # p1_12.plot(x=x_df, y=df['renko1_6평균'], pen=(20,  50, 150),name='renko6')
        # p1_12.plot(x=x_df, y=df['renko1_9평균'], pen=(242, 203, 95),name='renko9')
        # p1_12.plot(x=x_df, y=df['renko1_12평균'], pen=(255,  0,  0),name='renko12')
        # p1_12.plot(x=x_df, y=df['renko1_20평균'], pen=(242, 203, 95),name='renko20')
        # p1_12.plot(x=x_df, y=df['renko1_40평균'], pen=(242, 203, 95),name='renko40')
        # p1_12.plot(x=x_df, y=df['renko1_60평균'], pen=(242, 203, 95),name='renko60')
        # p1_12.plot(x=x_df, y=df['renko1_bricks'], pen=(92, 210, 229),name='renko_bricks')
        # p12.plot(x=xValue, y=df['매도잔량2평균최고'], pen=(y_dot), name='매도잔량2평균최고')

        # lr = pg.LinearRegionItem([5, 1000])
        # lr.setZValue(-1)
        # p2.addItem(lr)

        p2_1.plot(x=x_df, y=df['high'  ], pen=r_dash,       name='high')
        p2_1.plot(x=x_df, y=df['low'  ], pen=r_dash,name='low')
        p2_1.plot(x=x_df, y=df['ma5'], pen=(120,200,200),name='ma5')
        p2_1.plot(x=x_df, y=df['ma60' ], pen=(120,150,150),name='ma60')
        p2_1.plot(x=x_df, y=df['ma60마지' ], pen=y_dot,name='ma60마지')
        p2_1.plot(x=x_df, y=df['ma300' ], pen=(128, 65,217),name='ma300')
        p2_1.plot(x=x_df, y=df['ma300마지' ], pen=g_dot,name='ma300마지')
        p2_1.plot(x=x_df, y=df['ma'], pen=(204,114, 61),name='ma')
        p2_1.plot(x=x_df, y=df['close'], pen=(200, 50, 50),name='close')

        # p1_2.plot(x=x_df, y=df['거래대금변동'], pen=g_dot,name='거래대금변동')
        # p2_2.plot(x=x_df, y=df['거래대금변동절대'],     pen=(120,200,200),name='거래대금변동절대')
        # p2_2.plot(x=x_df, y=df['거래대금변동평균' ],pen=(0, 250, 0),name='거래대금변동평균')
        # p2_2.plot(x=x_df, y=df['거래대금평균최고' ],pen=(200, 50, 50),name='거래대금평균최고')
        # p2_2.plot(x=x_df, y=df['거래대금평균최고마지' ],pen=(128, 65,217),name='거래대금평균최고마지')
        # p2_2.plot(x=x_df, y=df['초대금평균차초대금평균최고' ],pen=(50, 50, 200),name='초대금평균차초대금평균최고')

        # p2_3.plot(x=x_df, y=df['ma' ],pen=(50, 50, 200),name='초대금평균차초대금평균최고')
        # p2_3.plot(x=x_df, y=df['hei_open'], pen=('r'), name='hei_open')

        p2_4.plot(x=x_df, y=df['cci' ],pen=(128, 65,217),name='cci')

        p2_5.plot(x=x_df, y=df['cmo' ],pen=(50, 50, 200),name='cmo')

        p2_6.plot(x=x_df, y=df['rsi' ],pen=(128, 65,217),name='rsi')
        p2_6.plot(x=x_df, y=df['rsi_upper' ],pen=(128, 65,217),name='rsi')
        p2_6.plot(x=x_df, y=df['rsi_lower' ],pen=(128, 65,217),name='rsi')

        p2_7.plot(x=x_df, y=df['band_upper' ],pen=(200, 50, 50),name='band_upper')
        p2_7.plot(x=x_df, y=df['band_middle'],pen=(128, 65,217),name='band_middle')
        p2_7.plot(x=x_df, y=df['band_lower' ],pen=(50, 50, 200),name='band_lower')


        p2_8.plot(x=x_df, y=df['atr' ],pen=(50, 50, 200),name='atr')

        # p2_9.plot(x=x_df, y=df['value'], pen=(255,  0,  0),name='value')

        # p2_10.plot(x=x_df, y=df['봉거래대금'], pen=(200, 50, 50), name='봉거래대금')
        # p2_10.plot(x=x_df, y=df['봉거래대금평균'], pen=y_dot, name='봉거래대금평균')
        # p2_10.plot(x=x_df, y=df['봉거래대금평균최고'], pen=(120, 200, 200), name='봉거래대금평균최고')

        # p2_11.plot(x=x_df, y=df['hei_close'], pen=('b'), name='hei_close')

        # p2_12.plot(x=x_df, y=df['renko1_3평균'], pen=(152, 20, 20), name='renko3')
        # p2_12.plot(x=x_df, y=df['renko1_6평균'], pen=(20, 50, 150), name='renko6')
        # p2_12.plot(x=x_df, y=df['renko1_9평균'], pen=(242, 203, 95), name='renko9')
        # p2_12.plot(x=x_df, y=df['renko1_12평균'], pen=(242, 203, 95), name='renko12')
        # p2_12.plot(x=x_df, y=df['renko1_20평균'], pen=(242, 203, 95), name='renko20')
        # p2_12.plot(x=x_df, y=df['renko1_40평균'], pen=(242, 203, 95), name='renko40')
        # p2_12.plot(x=x_df, y=df['renko1_60평균'], pen=(242, 203, 95), name='renko9')
        # p2_12.plot(x=x_df, y=df['renko1_bricks'], pen=(92, 210, 229), name='renko_bricks')




        crosshair1(main_pg=p1_1, sub_pg1=p1_2, sub_pg2=p1_3,sub_pg3=p1_4,sub_pg4=p1_5,sub_pg5=p1_6,sub_pg6=p1_7,sub_pg7=p1_8,sub_pg8=p1_9,sub_pg9=p1_10,sub_pg10=p1_11,sub_pg11=p1_12)
        crosshair2(main_pg=p2_1, sub_pg1=p2_2, sub_pg2=p2_3,sub_pg3=p2_4,sub_pg4=p2_5,sub_pg5=p2_6,sub_pg6=p2_7,sub_pg7=p2_8,sub_pg8=p2_9,sub_pg9=p2_10,sub_pg10=p2_11,sub_pg11=p2_12)

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.df = data
        self.generatePicture()
        print(self.df)
    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)

        for i in range(len(self.df)):
            index = self.df.index[i]
            unix_ts = index.timestamp()
            open  = self.df.loc[index]['open']
            high  = self.df.loc[index]['high']
            low   = self.df.loc[index]['low']
            close = self.df.loc[index]['close']

            if close >= open:
                p.setPen(pg.mkPen(color='r'))
                p.setBrush(pg.mkBrush(color='r'))
            else:
                p.setPen(pg.mkPen(color='b'))
                p.setBrush(pg.mkBrush(color='b'))

            p.drawLine(QPointF(i, high), QPointF(i, low))
            p.drawRect(QRectF(i-0.25, open, 0.5, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

class HeikinItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.df = data
        self.generatePicture()
        print(self.df)
    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)

        for i in range(len(self.df)):
            index = self.df.index[i]
            # unix_ts = index.timestamp()
            open  = self.df.loc[index]['hei_open']
            high  = self.df.loc[index]['hei_high']
            low   = self.df.loc[index]['hei_low']
            close = self.df.loc[index]['hei_close']

            if close >= open:
                p.setPen(pg.mkPen(color='r'))
                p.setBrush(pg.mkBrush(color='r'))
            else:
                p.setPen(pg.mkPen(color='b'))
                p.setBrush(pg.mkBrush(color='b'))

            p.drawLine(QPointF(i, high), QPointF(i, low))
            p.drawRect(QRectF(i-0.25, open, 0.5, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())


def df_add(df):
    avgtime = 30
    # 체결강도max = 1000
    # 체결강도min = 60

    # df.drop(df.loc[df['시가']<1].index, inplace=True) #시가가 1보다 작은 행은 결측으로 처리하여 삭제
    # df.loc[df["체결강도"] > 체결강도max, "체결강도"] = 체결강도max #체결강도가 체결강도max 넘어가는 값은 max 값 으로 변경
    # df.loc[df["체결강도"] < 체결강도min, "체결강도"] = 체결강도min #체결강도가 체결강도min 넘어가는 값은 max 값 으로 변경

    # df['당일거래대금'] = df['당일거래대금'] / 100
    # print(df)
    df['고저평균대비등락율'] = (df['close'] / ((df['high'] + df['low']) / 2) - 1) * 100
    df['고저평균대비등락율'] = df['고저평균대비등락율'].round(2)

    df['최고등락'] = (df['high']-df['low'])/df['low']*100
    df['최고등락평균'] = df['최고등락'].rolling(window=60).mean().round(3)
    df['등락'] = (df['close']-df['open'])/df['open']*100
    df['등락평균'] = df['등락'].rolling(window=60).mean().round(3)

    # df['체결강도평균'] = df['체결강도'].rolling(window=avgtime).mean()
    # df['체결강도평균'] = df['체결강도평균'].round(3)
    #
    # df['체강차체강평균'] = df['체결강도'] - df['체결강도평균']
    # df['체강차체강평균최저'] = (df['체결강도'] - df['체결강도평균']).rolling(window=avgtime).min()
    # df['체강차체강평균최고'] = (df['체결강도'] - df['체결강도평균']).rolling(window=avgtime).max()
    #
    # df['체결강도평균120'] = df['체결강도'].rolling(window=120).mean()
    # df['체결강도평균120'] = df['체결강도평균120'].round(3)
    #
    # df['체결강도평균마지+'] = df['체결강도평균'] *1.05
    #
    # df['체결강도평균마지-'] = df['체결강도평균'] *0.95
    #
    # df['체결강도최고'] = df['체결강도'].rolling(window=avgtime).max()
    # df['체결강도최고'] = df['체결강도최고'].round(3)

    # df['직전당일거래대금'] = df['당일거래대금'].shift(1)
    # df['거래대금차'] = df['value'] - df['value'].shift(1)
    # df['거래대금차'].iloc[0] = 0  # 초반 튀는값 잡기위해

    # df['거래대금차평균'] = df['거래대금차'].rolling(window=avgtime).mean().round(3)
    # df['초당거래대금평균'] = df['초당거래대금평균'].round(3)
    # df.loc[df["초당거래대금평균"] > 거래대금max, "초당거래대금평균"] = 거래대금max
    # df.loc[df["초당거래대금평균"] < 거래대금min, "초당거래대금평균"] = 거래대금min

    # df['직전거래대금차'] = df['거래대금차'].shift(1)
    # df['거래대금변동'] = (df['직전거래대금차'] - df['거래대금차'])
    # df.loc[df["초당거래대금변동"] > 거래대금max, "초당거래대금변동"] = 거래대금max
    # df.loc[df["초당거래대금변동"] < 거래대금min, "초당거래대금변동"] = 거래대금min

    # df['거래대금변동절대'] = abs(df['직전거래대금차'] - df['거래대금차'])
    df['거래대금변동평균'] = df['거래대금변동절대'].rolling(window=avgtime).mean().round(3)
    # df.loc[df["초당거래대금변동절대"] > 거래대금max, "초당거래대금변동절대"] = 거래대금max
    # df.loc[df["초당거래대금변동절대"] < 거래대금min, "초당거래대금변동절대"] = 거래대금min


    df['거래대금평균최고'] = df['거래대금차평균'].rolling(window=avgtime).max()
    df['거래대금평균최고'] = df['거래대금평균최고'].round(3)
    df['거래대금평균최고마지'] = df['거래대금평균최고']*0.9
    # df.loc[df["초당거래대금평균최고"] > 거래대금max, "초당거래대금평균최고"] = 거래대금max
    # df.loc[df["초당거래대금평균최고"] < 거래대금min, "초당거래대금평균최고"] = 거래대금min
    df['초대금평균차초대금평균최고'] = abs(df['거래대금차평균'] - df['거래대금평균최고'])

    df['거래대금평균60'] = df['거래대금차'].rolling(window=60).mean()
    df['거래대금평균60'] = df['거래대금평균60'].round(3)

    df['거래대금평균120'] = df['거래대금차'].rolling(window=120).mean()
    df['거래대금평균120'] = df['거래대금평균120'].round(3)

    df['거래대금각도'] = np.arctan((df['value']-df['value'].shift(1))/1000) * 180 / np.pi

    df['봉거래대금'] = df['close'] * df['volume']

    df['봉거래대금평균'] = df['봉거래대금'].rolling(window=avgtime).mean().round(3)
    # df['초당매수대금평균'] = df['초당매수대금평균'].round(3)

    # df['초당매도대금평균'] = df['초당매도대금'].rolling(window=avgtime).mean()
    # df['초당매도대금평균'] = df['초당매도대금평균'].round(3)

    df['봉거래대금평균최고'] = df['봉거래대금평균'].rolling(window=avgtime).max().round(3)

    # df['초당매도대금평균최고'] = df['초당매도대금평균'].rolling(window=avgtime).max()
    # df['초당매도대금평균최고'] = df['초당매도대금평균최고'].round(3)



    # df['매수가'] = np.nan
    # df['매도가'] = np.nan
    # df.to_csv(path+'/database/' + stock_name + ".csv", header=True, index=True, encoding='utf-8-sig')
    return df
def show_chart(df, stock_name,stock_code,date,end):
    df = df_add(df)
    window=Window(df,stock_name,stock_code,date,end)

    return window
if __name__ == '__main__':
    path = "D:/tele_bot/"
    macro_file = path + 'macroeconomics.db'
    KRX_file = path + 'KRX.db'
    US_stock_file = path + 'US_stock.db'
    con = sqlite3.connect(macro_file)
    table = 'KRX100'
    df = pd.read_sql(f"SELECT * FROM '{table}'", con).set_index('index')
    # df = pd.read_sql("SELECT * FROM " + "'" + table + "'", con).set_index('index')
    # df.index = df.index.strftime("%Y%m%d%H%M%S").astype(np.int64)
    print(df)
    # con.commit()
    # con.close()
    # df = df_add(df)
    df = make_indicator.heikin_ashi(df)
    df = make_indicator.sma(df)
    df = make_indicator.CCI(df)
    df = make_indicator.CMO(df)
    df = make_indicator.RSI(df)
    df = make_indicator.BBAND(df)
    df = make_indicator.ATR(df)
    # df = make_indicator.renko_sma(df)
    df['수익률'] = df['close'].pct_change() + 1
    avgtime=30
    # quit()
    # df = df_backtest(stock_name,df,date,start,end,back_file)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtWidgets.QApplication(sys.argv)
        # ticker = table[table.find('-')+1:table.find('_')] #테이블명의 '-'와'_'
        # candle = table[table.find('_')+1:]
        window = Window(df, table)
        window.setGeometry(0, 30, 3850, 1010)
        window.show()
        # QtGui.QApplication.instance().exec_()
        sys.exit(app.exec_())
        # QTest.qWait(5000)
        # window.close()
    # show_chart()

