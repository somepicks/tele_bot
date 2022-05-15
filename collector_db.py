#https://financedata.github.io/FinanceDataReader/
import pyupbit
import pandas as pd
import numpy as np
import sqlite3
import make_indicator
pd.set_option('display.max_columns',None) #모든 열을 보고자 할 때
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width',1500)
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option('mode.chained_assignment',  None) # SettingWithCopyWarning 경고를 끈다
import FinanceDataReader as fdr

def list_krx():
    con = sqlite3.connect(db_file)
    stock_list = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    stock_list.종목코드 = stock_list.종목코드.map('{:06d}'.format)  # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    stock_list = stock_list[['회사명', '종목코드', '업종', '주요제품', '상장일']]  # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
    print(stock_list)
    df_etf = fdr.StockListing('ETF/KR')
    print(df_etf)
    df_krx = fdr.StockListing('KRX')
    print(df_krx)

    return df_krx

def list_US():
    stocks = fdr.StockListing('NYSE')  # 뉴욕거래소
    stocks = fdr.StockListing('NASDAQ')  # 나스닥
    stocks = fdr.StockListing('AMEX')  # 아멕스

def make_db(stocks,file):
    tickers=list(stocks.keys())
    name = list(stocks.values())
    table_list = get_table_list(file)
    for i,ticker in enumerate(tickers):
        print(f'DB저장 중... [{i+1}:{len(tickers)}] | {name[i]}')
        con = sqlite3.connect(file)
        # cur = con.cursor()
        table = name[i]
        if table in table_list:
            df_exist = pd.read_sql(f"SELECT * FROM '{table}'", con).set_index('index')
            print(df_exist.index)
            df = fdr.DataReader(symbol=ticker,start='2022')
            df.index = df.index.strftime("%Y%m%d").astype(np.int64)
            print(df.index)
            df = df[df.index > df_exist.index[-1]]  # 중복이 아닌 df만 받아오기
            print(df.index)
        else:
            df = fdr.DataReader(symbol=ticker)

        df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume','Change':'change'}, inplace=True)  # 컬럼명 변경
        # df = make_indicator.sma(df)
        # df = make_indicator.CCI(df)
        # df = make_indicator.CMO(df)
        # df = make_indicator.RSI(df)
        # df = make_indicator.df_add(df)
        # df = make_indicator.BBAND(df)
        # df = make_indicator.ATR(df)
        # df = make_indicator.heikin_ashi(df)
        # print(df)
        df.index = df.index.strftime("%Y%m%d").astype(np.int64)
        df.to_sql(table, con, if_exists='append')

        con.commit()
        con.close()
def get_table_list(file):
    con = sqlite3.connect(file)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = cursor.fetchall()  # fetchall 한번에 모든 로우 데이터 읽기 (종목코드 읽기)
    if not table_list:
        print('* DB 테이블이 비어있음 - 확인 필요 *')
        table_list = []
        return table_list
    else:
        table_list = np.concatenate(table_list).tolist()
        return table_list
if __name__ == '__main__':
    index ={'KS11':'코스피','KQ11':'코스닥','KS50':'코스피50','KS100':'코스피100','KRX100':'KRX100','KS200':'코스피200'
              ,'DJI':'다우존스','US500':'S&P500','VIX':'VIX','STOXX50E':'유로스톡50','CSI300':'중국','HSI':'항셍'
              ,'FTSE':'영국','DAX':'독일','CAC':'프랑스'}
    bond ={'KR1YT=RR':'한국국채1년','KR10YT=RR':'한국국채10년','US1MT=X':'미국국채1개월','US10YT=X':'미국국채10년'
        ,'US3MT=X':'미국국채3개월','US2YT=X':'미국국채2년'}
    exchange ={'AUD/CHF':'호주/스위스','USD/KRW':'미국/한국','USD/EUR':'미국/유로','USD/JPY':'미국/엔화','CNY/KRW':'중국/한국'
        ,'EUR/USD':'유로/달러','JPY/KRW':'일본/한국','AUD/USD':'호주/미국','EUR/JPY':'유로/일본','USD/RUB':'미국/러시아'}
    materials ={'NG':'천연가스','ZG':'금','ZI':'은','HG':'구리'}
    US = {'TBT':'TBT','NRGU':'NRGU','NRGD':'NRGD','TQQQ':'TQQQ','SQQQ':'SQQQ'}
    KRX = {'010950':'에스오일','005930':'삼성전자','123320':'TIGER 레버리지'}
    indicator = dict(index,**bond,**exchange,**materials) # 딕셔너리 병합
    US = dict(**US) # 딕셔너리 병합
    KRX = dict(**KRX) # 딕셔너리 병합
    db_file = "D:/db_files/data.db"
    KRX_file = "D:/db_files/KRX.db"
    make_db(indicator,db_file)
    # make_db(indicator,KRX_file)