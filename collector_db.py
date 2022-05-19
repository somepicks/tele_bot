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
import pandas_datareader as pdr
def krx_list():
    df1 = fdr.StockListing('KOSPI')
    index_x = df1[df1['Sector'].isnull()].index  # sector가 null인 행 찾아서 지우기
    df1.drop(index_x, inplace=True)
    # print(df1)
    # df1['Sector'].groupby
    df2 = fdr.StockListing('KOSDAQ')
    index_x = df2[df2['Sector'].isnull()].index  # sector가 null인 행 찾아서 지우기
    df2.drop(index_x, inplace=True)
    df = pd.concat([df1, df2], axis=0)
    stock_name = df['Name'].tolist()
    stock_code = df['Symbol'].tolist()
    stocks = dict(zip(stock_code,stock_name)) #리스트로 딕셔너리 만들기
    stocks['123320']='TIGER 레버리지'
    stocks['091220']='TIGER 은행'
    stocks['091230']='TIGER 반도체'
    stocks['098560']='TIGER 방송통신'
    stocks['139220']='TIGER 200 건설'
    stocks['139230']='TIGER 200 중공업'
    stocks['139240']='TIGER 200 철강소재'
    stocks['139250']='TIGER 200 에너리화학'
    stocks['139260']='TIGER 200 IT'
    stocks['139270']='TIGER 200 금융'
    stocks['143860']='TIGER 헬스케어'
    stocks['157490']='TIGER 소프트웨어'
    stocks['157500']='TIGER 증권'
    stocks['228790']='TIGER 화장품'
    stocks['228800']='TIGER 여행레저'
    return stocks
def US_list():
    stocks = fdr.StockListing('NYSE')  # 뉴욕거래소
    stocks = fdr.StockListing('NASDAQ')  # 나스닥
    stocks = fdr.StockListing('AMEX')  # 아멕스
    US = {'TBT':'TBT','NRGU':'NRGU','NRGD':'NRGD','TQQQ':'TQQQ','SQQQ':'SQQQ','DBA':'미국농산물',
          'CORN':'미국옥수수','SOYB':'미국콩','JO':'미국커피','WEAT':'미국밀','MOO':'미국농업'}
    return US
def index_list():
    index ={'KS11':'코스피','KQ11':'코스닥','KS50':'코스피50','KS100':'코스피100','KRX100':'KRX100','KS200':'코스피200'
              ,'DJI':'다우존스','US500':'S&P500','VIX':'VIX','CSI300':'중국','HSI':'항셍'
              ,'FTSE':'영국','DAX':'독일','CAC':'프랑스'}
    bond ={'KR1YT=RR':'한국국채1년','KR10YT=RR':'한국국채10년','US1MT=X':'미국국채1개월','US10YT=X':'미국국채10년'
        ,'US3MT=X':'미국국채3개월','US2YT=X':'미국국채2년'}
    exchange ={'AUD/CHF':'호주/스위스','USD/KRW':'미국/한국','USD/EUR':'미국/유로','USD/JPY':'미국/엔화','CNY/KRW':'중국/한국'
        ,'EUR/USD':'유로/달러','JPY/KRW':'일본/한국','AUD/USD':'호주/미국','EUR/JPY':'유로/일본','USD/RUB':'미국/러시아'}
    materials ={'NG':'천연가스','ZG':'금','ZI':'은','HG':'구리'}
    # 'STOXX50E':'유로스톡50',
    indicator = dict(index,**bond,**exchange,**materials) # 딕셔너리 병합
    return indicator
def fred_list():
    FRED = {'M2':'M2통화량','NASDAQCOM':'나스닥종합','HSN1F':'주택판매지수','GS10':'gs10',"XTEXVA01KRM667N":'수출'}
    # , 'gs10': 'gs10'
    return FRED
def make_db(stocks,file):
    tickers=list(stocks.keys())
    name = list(stocks.values())
    table_list = get_table_list(file)
    for i,ticker in enumerate(tickers):
        print(f'DB저장 중... [{i+1}:{len(tickers)}] | {name[i]}...',end='')
        con = sqlite3.connect(file)
        # cur = con.cursor()
        table = name[i]
        if table in table_list:
            df_exist = pd.read_sql(f"SELECT * FROM '{table}'", con).set_index('index')
            # print(df_exist.index)
            try:
                df = fdr.DataReader(symbol=ticker,start='2022')
            except:
                df = pdr.DataReader(ticker,start='2022')
            df.index = df.index.strftime("%Y%m%d").astype(np.int64)
            # print(df.index)
            df = df[df.index > df_exist.index[-1]]  # 중복이 아닌 df만 받아오기
            if df.empty:
                continue
        else:
            df = fdr.DataReader(symbol=ticker)
            df.index = df.index.strftime("%Y%m%d").astype(np.int64)
        df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume','Change':'change'}, inplace=True)  # 컬럼명 변경
        df.index.name = 'index' #인덱스명 변경
        df.to_sql(table, con, if_exists='append')
        con.commit()
        con.close()
        print('[완료]')
def make_db_pdr(stocks,file):
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
            # print(df_exist.index)
            df = pdr.get_data_yahoo(ticker,start=start,end=end)
            df.index = df.index.strftime("%Y%m%d").astype(np.int64)
            # print(df.index)
            df = df[df.index > df_exist.index[-1]]  # 중복이 아닌 df만 받아오기
            if df.empty:
                continue
        else:
            df = pdr.get_data_yahoo(ticker,start=start,end=end)
        df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume','Change':'change'}, inplace=True)  # 컬럼명 변경
        df.index.name = 'index' #인덱스명 변경
        df.index = df.index.strftime("%Y%m%d").astype(np.int64)
        df.to_sql(table, con, if_exists='append')
        con.commit()
        con.close()
def make_fred_db(stocks,file):
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
            # print(df_exist.index)
            df = fdr.DataReader(symbol=ticker,data_source='fred')
            df.index = df.index.strftime("%Y%m%d").astype(np.int64)
            # print(df.index)
            df = df[df.index > df_exist.index[-1]]  # 중복이 아닌 df만 받아오기
            if df.empty:
                continue
        else:
            df = fdr.DataReader(symbol=ticker,data_source='fred')
            df.index = df.index.strftime("%Y%m%d").astype(np.int64)
        df.rename(columns={ticker:'close'}, inplace=True)  # 컬럼명 변경
        df.index.name = 'index' #인덱스명 변경
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
    db_file = "D:/db_files/data.db"
    KRX_file = "D:/db_files/KRX.db"
    US_file = "D:/db_files/US.db"
    start = '2010-01-01'
    end = '2022-05-15'

    # get_table_list(db_file)
    # make_db(index_list(),db_file)
    # make_fred_db(fred_list(),db_file)
    make_db(krx_list(),KRX_file)
    # make_db_pdr(US_list(),US_file)