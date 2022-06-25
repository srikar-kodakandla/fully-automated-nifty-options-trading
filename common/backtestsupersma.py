from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
from common.indicator import SuperTrend


from fyers.accounts_login import login_accounts
from common.indicator import SuperTrend
from time import sleep
import time
from common import message as m
import sys
from fyers.order import order
import datetime
from fyers.script import name_to_script
from fyers.quote import quote
from fyers.stoploss_percentage import percentage
from fyers.live import full_data
import pandas as pd
import os
from time import sleep
import ta
stock_name='NSE:NIFTY50-INDEX'
name_script=name_to_script(stock_name)
accounts=login_accounts()
l=full_data(accounts[0])
#data=l.full_data(stock_name)
data=l.full_data(stock_name,resolution=5,days=98)
data = pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv', parse_dates=True)
#data=data[-30000:]
data = data.dropna()
#data.columns=['Open', 'High', 'Low', 'Close']
data=data.set_index('Date')
#data=data.set_index('ts')
data.index=pd.to_datetime(data.index)
#data=data[-8000:]
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator
#from common.indicator import SuperTrend
import numpy as np
from tqdm import tqdm 

from backtesting.test import SMA

bar=tqdm(total=7600*10/4)

hhh = pd.DataFrame()
it = 0


def rs(data):
    #global hhh
    #global it
    if len(hhh) == 0:
        hhh = ADXIndicator(low=data['Low'], close=data['Close'], high=data['High']).adx()
        # hhh=RSIIndicator(data['Close']).rsi()
    # print(data)
    # print(data)
    #it += 1
    #print(it)
    return hhh

    # return ADXIndicator(low=data['Low'],close=data['Close'],high=data['High']).adx()


def st(period, multiplier, data):
    global bar
    bar.update(1)
    p = SuperTrend(data, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close'])
    # trend=p['STX_80_3.6']
    # trend[trend=='down']=0
    # trend[trend=='up']=1
    # trend[trend=='nan']=np.nan
    return p[f'ST_{period}_{multiplier}']


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    #print(n)
    return pd.Series(values).rolling(n).mean()
class SmaCross(Strategy):
    period = 480
    multiplier = 16.4
    n1=200
    n2=200
    def init(self):
        price = self.data.Close
        # self.ma1 = self.I(SMA, price, 50)
        # self.ma2 = self.I(SMA, price, 200)
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)
        self.trend = self.I(st, self.period, self.multiplier, self.data.df)
        #self.rsi = self.I(rs, self.data.df)
        # self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        # self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)

    def next(self):
        if self.trend <= self.data.Close and not self.position.is_long:
            self.position.close()
            #if self.rsi > self.h:
            if self.sma1>self.data.Close:
                self.buy()
        elif self.trend >= self.data.Close and not self.position.is_short:
            self.position.close()
            #if self.rsi < self.h:
            if self.sma1<self.data.Close:
                self.sell()
bt = Backtest(data, SmaCross, commission=0.002, trade_on_close=False, cash=1000000000000, exclusive_orders=True)

stats = bt.run()
bt.plot()
import numpy as np


stats = bt.optimize(#period=range(5, 1000, 1),
    #multiplier=np.arange(5,30,0.1).tolist(),
    n1=range(1,1000,1),
    #n2=range(1,1000,10),
    #h=range(1, 100, 5),
    maximize='Win Rate [%]', return_heatmap=True,max_tries=2000)

bt.plot()




def next(self):
    if self.trend == 0 and not self.position.is_long:
        self.position.close()
        self.buy()
    elif self.trend == 1 and not self.position.is_short:
        self.position.close()
        self.sell()