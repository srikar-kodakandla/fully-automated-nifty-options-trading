import os
from common import message as m
import pandas as pd
from time import gmtime, strftime
import time
from datetime import timedelta

from pandas.io.parsers import read_csv
start_time = time.monotonic()
try:
    read=open('stock_selection.txt','r')
except:
    read = open('fyers/stock_selection.txt', 'r')
stock=read.read().split('\n')
read.close()
from fyers.accounts_login import login_accounts
from fyers.script import name_to_script
from fyers.live import full_data
d = pd.DataFrame(columns=('name','period', 'multiplier', 'buy', 'sell', 'total'))
accounts=login_accounts()
a=full_data(accounts[0])

#stock_name=stock[0]
'''for stock_name in stock:
    name_script=name_to_script(stock_name)
    if name_script=='NSE:20MICRONS-EQ':
        continue
    print(name_script)
    try:
        data=a.full_data(name_script,days=98)
    except Exception as error:
        m.message("Data is not availible from fyers server to search optimized value for given stock {name_script} , Trying to request for less data ... ") 
        try:
            data=a.full_data(name_script,days=90)
        except:
            m.message("Final Call , it won't try again ... , Data is not availible from fyers server to search optimized value for given stock {name_script} ") 
 '''           
    #realdata = data.copy()
for ii in range(1,1000):
    d = pd.DataFrame(columns=('name','period', 'multiplier', 'buy', 'sell', 'total'))
    for stock_name in stock:   
        name_script=name_to_script(stock_name)
        print(name_script)
        if name_script=='NSE:20MICRONS-EQ':
            continue
        try:
            data=a.full_data(name_script,days=98)
        except Exception as error:
            #m.message(f"Data is not availible from fyers server to search optimized value for given stock {name_script} , Trying to request for less data ... ") 
            try:
                data=a.full_data(name_script,days=90)
            except:
                print(f"Exception occured, data is not there for the following stock {name_script}")
                #m.message(f"Final Call , it won't try again ... , Data is not availible from fyers server to search optimized value for given stock {name_script} ") 
                continue
        #m.message(f'searching for supertrend value for {name_script} stock , It takes approximately 15 to 20 hours to find optimized value of supertrend for any stock , you will get message after searching is completed')
        from common.indicator import *
        import numpy as np
        

        def calculate(a, b, data1, d=d):
            # b = 0
            # data1=realdata.copy()
            #for b in np.arange(4,7, 0.1):
            t = SuperTrend(data1, a, b).iloc[2000:]
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
                    if trend[i] == 'down':#and trend[i - 1] == 'up':
                        sellposition = close[i]
                if buyposition == 0:
                    if trend[i] == 'up': #and trend[i - 1] == 'down':
                        buyposition = close[i]
                if trend[i] == 'down' and trend[i - 1] == 'up' and buyposition != 0:
                    buyprofit = close[i] - buyposition + buyprofit
                    # print(buyprofit)
                    sellposition = close[i]
                    sell.append(buyprofit)
                if trend[i] == 'up' and trend[i - 1] == 'down' and sellposition != 0:
                    sellprofit = sellposition - close[i] + sellprofit
                    # print(sellprofit)
                    buyposition = close[i]
                    buy.append(sellprofit)
            try:

                if trend[-1]=='up':
                    buyprofit = close[-1] - buyposition + buyprofit
                    buy.append(buyprofit)
                if trend[-1]=='down':
                    sellprofit = sellposition - close[-1] + sellprofit
                    sell.append(sellprofit)
            except:
                print("There is no data to calculate function")        

            # plt.plot(sell)
            # plt.plot(buy)
            nnn=name_script.split(':')[1].split('-')[0]
            #total=(total/close[i])*100
            try:
                buyprofit=(buyprofit/close[0])*100
                sellprofit=(sellprofit/close[0])*100
                #sellprofit
                d = d.append(
                    {'name':nnn,'period': a, 'multiplier': b, 'buy': buyprofit, 'sell': sellprofit, 'total': buyprofit + sellprofit},
                    ignore_index=True)
                    #print([a, b, buyprofit, sellprofit, buyprofit + sellprofit])
                return d
            except Exception as error:
                print(error)    
        d=d.append(calculate(544,4.5,data[-2000-375*(ii+1):-375*(ii)]))
        d=d.drop_duplicates()
        d=d.sort_values(by='total',ascending=False)
        print(d)
        d.to_csv(f'oneday_csv/{ii}.csv')
