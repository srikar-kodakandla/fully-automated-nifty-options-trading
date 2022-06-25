
from common.indicator import SuperTrend



from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

data = pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv', parse_dates=True)
data = data.dropna()
#data = data[-20000:]
import pandas as pd
from ta.momentum import RSIIndicator
import bt
data = data.dropna()
#data.columns=['Open', 'High', 'Low', 'Close']
data=data.set_index('Date')
#data=data.set_index('ts')
data.index=pd.to_datetime(data.index)
rr=0
# RSIIndicator(data['Close']).rsi()
def rs(data):
    #print(data)
    global rr
    if type(rr)==int:
        rr= RSIIndicator(data['Close']).rsi()
    return rr    
from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

import pandas as pd
# data=data[-8000:]
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator
#from common.indicator import SuperTrend
import numpy as np
from tqdm import tqdm

bar=tqdm(total=100*100/4)

hhh = pd.DataFrame()
it = 0


'''def rs(data):
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
'''
    # return ADXIndicator(low=data['Low'],close=data['Close'],high=data['High']).adx()

p=0
def st(period, multiplier, data):
    global bar
    global p
    bar.update(1)
    if type(p)==int:
        p = SuperTrend(data, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close'])
    # trend=p['STX_80_3.6']
    # trend[trend=='down']=0
    # trend[trend=='up']=1
    # trend[trend=='nan']=np.nan
    return p[f'ST_{period}_{multiplier}']
i=0
p=0
def st1(period, multiplier, data):
    global bar
    global p
    global i
    bar.update(1)
    if type(p)==int or type(i)==int:
        p = SuperTrend(data, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close'])
        i=p[f'STX_{period}_{multiplier}']
        i[i=='down']=0
        i[i=='up']=1
    # trend=p['STX_80_3.6']
    # trend[trend=='down']=0
    # trend[trend=='up']=1
    # trend[trend=='nan']=np.nan
    return i

class SmaCross(Strategy):
    period = 38
    multiplier = 12.5
    buyrsi=45
    sellrsi=15
    def init(self):
        price = self.data.Close
        # self.ma1 = self.I(SMA, price, 50)
        # self.ma2 = self.I(SMA, price, 200)
        self.trend = self.I(st, self.period, self.multiplier, self.data.df,plot=False)
        self.rsi = self.I(rs, self.data.df,plot=False)
        self.trend1=self.I(st1,self.period,self.multiplier,self.data.df,plot=False)
        # self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        # self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)

    def next(self):
        if self.trend <= self.data.Close and not self.position.is_long:
            self.position.close()
            #if self.rsi > self.h:
            if self.buyrsi<self.rsi and self.trend1[-2]==0:
                self.buy()
        elif self.trend >= self.data.Close and not self.position.is_short:
            self.position.close()
            if self.sellrsi>self.rsi and self.trend1[-2]==1:
                self.sell()
bt = Backtest(data, SmaCross, commission=0.002, trade_on_close=False, cash=1000000000000, exclusive_orders=True)

stats1 = bt.run()
bt.plot(resample=False)
import numpy as np


stats = bt.optimize(#period=range(5, 1000, 5),
    #multiplier=np.arange(5,50,0.5).tolist(),
    #h=range(1, 100, 5),
    buyrsi=range(1,100),
    sellrsi=range(1,100),
    maximize='Win Rate [%]', return_heatmap=True)
