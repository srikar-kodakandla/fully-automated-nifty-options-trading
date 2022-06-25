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
data.columns=['Open','High','Low','Close']
#data = pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv', parse_dates=True)
#data=data[-30000:]

#data.columns=['Open', 'High', 'Low', 'Close']
#data=data.set_index('Date')
#data=data.set_index('ts')
#data.index=pd.to_datetime(data.index)
# data=data[-8000:]
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator
#from common.indicator import SuperTrend
import numpy as np
from tqdm import tqdm 
bar=tqdm(total=12000/4)
hhh = pd.DataFrame()
it = 0
def rs(data):
    global hhh
    global it
    if len(hhh) == 0:
        hhh = ADXIndicator(low=data['Low'], close=data['Close'], high=data['High']).adx()
        # hhh=RSIIndicator(data['Close']).rsi()
    # print(data)
    # print(data)
    it += 1
    print(it)
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
    y=p[f'STX_{period}_{multiplier}']
    y[y=='up']=1
    y[y=='down']=0
    return p[f'STX_{period}_{multiplier}']
def st1(period, multiplier, data):
    global bar
    bar.update(1)
    p = SuperTrend(data, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close'])
    # trend=p['STX_80_3.6']
    # trend[trend=='down']=0
    # trend[trend=='up']=1
    # trend[trend=='nan']=np.nan
    return p[f'ST_{period}_{multiplier}']

def vix():
    global data1
    return data1['Close']
import pdb
class SmaCross(Strategy):
    period =147
    multiplier = 13.9
    period1=142
    multiplier1=12.8
    v=30
    def init(self):
        price = self.data.Close
        # self.ma1 = self.I(SMA, price, 50)
        # self.ma2 = self.I(SMA, price, 200)
        self.trend =self.I( st, self.period, self.multiplier, self.data.df,plot=False)
        #self.trend1 =self.I(st, self.period1, self.multiplier1, self.data.df,plot=False)
        self.tren =self.I( st1, self.period, self.multiplier, self.data.df)
        #self.tre =self.I(st1, self.period1, self.multiplier1, self.data.df)
        #self.vix=self.I(vix)
        #self.rsi = self.I(rs, self.data.df)
        # self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        # self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)
        
    def next(self):
        #print(self.trend)
        #pdb.set_trace()
        if (self.trend[-2]==1 and self.trend[-1]==0)  and not self.position.is_short:
            #self.position.close()
            #if self.rsi < self.h:
            #if self.vix>self.v:
            self.sell()
        if (self.trend[-2]==0 and self.trend[-1]==1) and not self.position.is_long:
            self.position.close()
class SmaCross1(Strategy):
    period =252
    multiplier = 13
    v=30
    def init(self):
        price = self.data.Close
        # self.ma1 = self.I(SMA, price, 50)
        # self.ma2 = self.I(SMA, price, 200)
        self.trend =self.I( st, self.period, self.multiplier, self.data.df,plot=False)
        #self.trend1 =self.I(st, self.period1, self.multiplier1, self.data.df,plot=False)
        self.tren =self.I( st1, self.period, self.multiplier, self.data.df)
        self.tre =self.I(st1, self.period1, self.multiplier1, self.data.df)
        #self.vix=self.I(vix)
        #self.rsi = self.I(rs, self.data.df)
        # self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        # self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)
        
    def next(self):
        #print(self.trend)
        #pdb.set_trace()
        if (self.trend[-2]==0 and self.trend[-1]==1) and not self.position.is_long:
            #self.position.close()
            #if self.rsi > self.h:
            #if self.vix>self.v:
            self.buy()
        if (self.trend[-2]==1 and self.trend[-1]==0) and not self.position.is_short:
            self.position.close()

data=pd.read_csv('https://drive.google.com/drive/folders/1TrRY8Al91F-xuWA7j2FQZWWfxRNNK1Mf')
bt = Backtest(data, SmaCross, commission=0.002, trade_on_close=False, cash=1000000000000, exclusive_orders=True)
import numpy as np
def test():
    stats1 = bt.run()
    #bt.plot()
    stats1 = bt.optimize(period=range(2, 500, 10),
        multiplier=np.arange(3,20,1).tolist(),
        #period1=range(2, 500, 10),
        #multiplier1=np.arange(3,20,1).tolist(),
        maximize='Win Rate [%]', return_heatmap=True,max_tries=400)
    print(stats1)
    try:
        bt.plot()
    except :
        pass
    return stats1[0]._strategy.period,round(stats1[0]._strategy.multiplier,3)




'''
def next(self):
    if self.trend == 0 and not self.position.is_long:
        self.position.close()
        self.buy()
    elif self.trend == 1 and not self.position.is_short:
        self.position.close()
        self.sell()'''