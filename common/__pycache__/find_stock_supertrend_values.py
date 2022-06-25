import os
from common import message as m
import pandas as pd
from time import gmtime, strftime
import time
from datetime import timedelta
start_time = time.monotonic()
try:
    read=open('stock_selection.txt','r')
except:
    read = open('fyers/stock_selection.txt', 'r')
stock_name=read.read().split('\n')
read.close()
stock_name=stock_name[0]
from fyers.accounts_login import login_accounts
from fyers.script import name_to_script
name_script=name_to_script(stock_name)
accounts=login_accounts()
print(name_script)
m.message(f'searching for supertrend value for {name_script} stock , It takes approximately 15 to 20 hours to find optimized value of supertrend for any stock , you will get message after searching is completed')
from fyers.live import full_data
a=full_data(accounts[0])
try:
    data=a.full_data(name_script,days=98)
except Exception as error:
    m.message("Data is not availible from fyers server to search optimized value for given stock {name_script} , Trying to request for less data ... ") 
    try:
        data=a.full_data(name_script,days=90)
    except:
        m.message("Final Call , it won't try again ... , Data is not availible from fyers server to search optimized value for given stock {name_script} ") 
        
realdata = data.copy()
from common.indicator import *
import numpy as np
d = pd.DataFrame(columns=('period', 'multiplier', 'buy', 'sell', 'total'))

def calculate(a, b, data1, d=d):
    b = 0
    # data1=realdata.copy()
    for b in np.arange(3,8, 0.1):
        t = SuperTrend(data1, a, b)
        (close, trend) = ((t['close'], t[f'STX_{a}_{b}']))
        close = close.to_numpy()
        trend = trend.to_numpy()
        buyposition = 0
        sellposition = 0
        buyprofit = 0
        sellprofit = 0
        sell = []
        buy = []
        for i in range(len(trend)):
            if sellposition == 0:
                if trend[i] == 'down' and trend[i - 1] == 'up':
                    sellposition = close[i]
            if buyposition == 0:
                if trend[i] == 'up' and trend[i - 1] == 'down':
                    buyposition = close[i]
            if trend[i] == 'down' and trend[i - 1] == 'up' and buyposition != 0:
                buyprofit = close[i] - buyposition + buyprofit
                # print(buyprofit)
                sellposition = close[i]
                sell.append(sellprofit)
            if trend[i] == 'up' and trend[i - 1] == 'down' and sellposition != 0:
                sellprofit = sellposition - close[i] + sellprofit
                # print(sellprofit)
                buyposition = close[i]
                buy.append(buyprofit)
        # plt.plot(sell)
        # plt.plot(buy)
        d = d.append(
            {'period': a, 'multiplier': b, 'buy': buyprofit, 'sell': sellprofit, 'total': buyprofit + sellprofit},
            ignore_index=True)
        print([a, b, buyprofit, sellprofit, buyprofit + sellprofit])
    return d

from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
results = Parallel(n_jobs=num_cores)(delayed(calculate)(j, 0, data) for j in range(40, 1000))

o = pd.DataFrame()
for i in results:
    o = o.append(i)
o=o.sort_values(['total'],ascending=[0])
pd.DataFrame(o).to_csv('supertrend_selection.csv')
pd.DataFrame(o).to_csv(f"supertrend_csv/{name_script.split(':')[1].split('-')[0]}.csv")
a=pd.read_csv('supertrend_selection.csv')
period=round(a['period'][100])
multiplier=round(a['multiplier'][100],1)
m.message(f"supertrend values are {period},{multiplier} for the stock {name_script}")
writ=open('supertrend_values.txt','w')
writ.write(str(period))
writ.write('\n')
writ.write(str(multiplier))
writ.close()
jjj=open(f"supertrend_txt/{name_script.split(':')[1].split('-')[0]}.txt",'w')
jjj.write(str(period))
jjj.write('\n')
jjj.write(str(multiplier))
jjj.close()
end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))
timetook=str(timedelta(seconds=end_time - start_time))
a=a[['period','multiplier','buy','sell','total']]
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    m.message(str(a.head(91)))

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    m.message(str(a.iloc[91:90+91]))
    
m.message(f"Time took to run the supertrend searching algorithm for {name_script.split(':')[1].split('-')[0]} stock is {timetook}")
print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
