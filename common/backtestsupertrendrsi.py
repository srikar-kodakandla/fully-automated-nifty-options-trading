from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
data=pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv',parse_dates=True)
data=data.dropna()
data=data[-8000:]
import pandas as pd
from ta.momentum import RSIIndicator
from common.indicator import SuperTrend
import numpy as np
def rs(data):
    #print(data)
    return RSIIndicator(pd.Series(data)).rsi()
def st(period,multiplier,data):
    p=SuperTrend(data,period,multiplier,ohlc=['Open', 'High', 'Low', 'Close'])
    #trend=p['STX_80_3.6']
    #trend[trend=='down']=0
    #trend[trend=='up']=1
    #trend[trend=='nan']=np.nan
    return p[f'ST_{period}_{multiplier}']
     
class SmaCross(Strategy):
    period=80
    multiplier=3.6
    h=80
    l=30
    def init(self):
        price = self.data.Close
        #self.ma1 = self.I(SMA, price, 50)
        #self.ma2 = self.I(SMA, price, 200)
        self.trend=self.I(st,self.period,self.multiplier,self.data.df)
        self.rsi = self.I(rs,self.data.Close)
        #self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        #self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)
    def next(self):
        if self.trend<=self.data.Close and not self.position.is_long:
            self.position.close()
            if self.rsi>self.h:
                self.buy()
        elif self.trend>=self.data.Close and not self.position.is_short:
            self.position.close()
            if self.rsi<self.l:
                self.sell()




bt = Backtest(data, SmaCross, commission=0.002,trade_on_close=True,cash=1000000000000,exclusive_orders=True)
stats = bt.run()
bt.plot()
import numpy as np
stats = bt.optimize(#period=range(5, 100, 1),
                    #multiplier=np.arange(3,10,0.1).tolist(),
                    h=range(1,100),
                    l=range(1,100),
                    maximize='Equity Final [$]')

def next(self):
    if self.trend==0 and not self.position.is_long:
        self.position.close()
        self.buy()
    elif self.trend==1 and not self.position.is_short:
        self.position.close()
        self.sell()