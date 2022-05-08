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
    con = sqlite3.connect('KRX.db')
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


def index_numbers():
    tickers ={'KS11':'코스피','KQ11':'코스닥','KS50':'코스피50','KS100':'코스피100','KRX100':'KRX100','KS200':'코스피200'
              ,'DJI':'다우존스','IXIC':'나스닥','US500':'S&P500','VIX':'VIX','STOXX50E':'유로스톡50','CSI300':'중국','HSI':'항셍'
              ,'FTSE':'영국','DAX':'독일','CAC':'프랑스'}

def bond():
    stocks ={'KR1YT=RR':'한국국채1년','KR10YT=RR':'한국국채10년','US1MT=X':'미국국채1개월','US10YT=X':'미국국채10년'
        ,'US3MT=X':'미국국채3개월','US2YT=X':'미국국채2년'}
    tickers=list(stocks.keys())
    name = list(stocks.values())
    for i,ticker in enumerate(tickers):
        print(f'DB저장 중... [{i+1}:{len(tickers)}] | {name[i]}')
        con = sqlite3.connect('bond.db')
        # cur = con.cursor()
        df = fdr.DataReader(ticker)
        df = make_indicator.sma(df)
        df = make_indicator.CCI(df)
        df = make_indicator.CMO(df)
        df = make_indicator.RSI(df)
        df = make_indicator.df_add(df)
        df = make_indicator.BBAND(df)
        df = make_indicator.ATR(df)
        df = make_indicator.heikin_ashi(df)
        df.index = df.index.strftime("%Y%m%d").astype(np.int64)
        df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Change':'change'}, inplace=True)  # 컬럼명 변경
        table = name[i]
        df.to_sql(table, con, if_exists='replace')
        con.commit()

def exchange():
    tickers ={'AUD/CHF':'호주/스위스','USD/KRW':'미국/한국','USD/EUR':'미국/유로','USD/JPY':'미국/엔화','CNY/KRW':'중국/한국'
        ,'EUR/USD':'유로/달러','JPY/KRW':'일본/한국','AUD/USD':'호주/미국','EUR/JPY':'유로/일본','USD/RUB':'미국/러시아'}

def materials():
    tickers ={'NG':'천연가스','ZG':'금','ZI':'은','HG':'구리'}


if __name__ == '__main__':
    # list_krx()
    bond()

