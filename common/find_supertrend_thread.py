import os
import pandas as pd
from time import gmtime, strftime
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
from fyers.live import full_data
a=full_data(accounts[0])
data=a.full_data(name_script,days=90)
realdata = data.copy()
from common.indicator import *
import numpy as np
d = pd.DataFrame(columns=('period', 'multiplier', 'buy', 'sell', 'total'))
def calculate(a, b, data1):
    # data1=realdata.copy()
    #for b in np.arange(1, 5, 0.1):
    global d
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
'''
from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()

print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
results = Parallel(n_jobs=num_cores)(delayed(calculate)(j, 0, data) for j in range(5, 500))
'''


from time import sleep

import threading
t=(calculate(80,3.6,data))
count=0
u=[]
for i in range(5,100):
    for j in np.arange(1, 5, 0.1):
        x=threading.Thread(target=calculate,args=(i, j, data))
        u.append(x)
        #x.start()
        count+=1
        print(count)
        #x.join()

print('threads completed')
sleep(1)

count=0
for i in u:
    count+=1
    print(count)
    print(d)
    i.start()
count=0
print('start completed')
sleep(1)
for i in u:
    count+=1
    print(count)
    i.join()
print('join completed')
#threading.Thread(target=calculate,args=(80,3.6, data)).start()
#t=(calculate(80,3.6,data))
o=d
'''
o = pd.DataFrame()
for i in results:
    o = o.append(i)'''
o=o.sort_values(['total'],ascending=[0])

pd.DataFrame(o).to_csv('supertrend_selection.csv')

print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
