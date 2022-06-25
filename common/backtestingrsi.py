from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
data=pd.read_csv('/home/ubuntu/Download/nifty_10min_data.csv',parse_dates=True)
data=data.dropna()
data=data[-20000:]
import pandas as pd
from ta.momentum import RSIIndicator
import bt
#RSIIndicator(data['Close']).rsi()
def rs(data):
    print(data)
    return RSIIndicator(pd.Series(data)).rsi()
class SmaCross(Strategy):
    l=20
    h=80
    def init(self):
        self.rsi = self.I(rs,self.data.Close)

    def next(self):
        if not self.position:
            if self.rsi < self.l:
                self.buy(size=1)
            else:
                self.sell(size=1)    
        
        if (self.rsi > self.h) and not self.position.is_short:
            
            self.sell(size=1)
        if (self.rsi < self.h) and not self.position.is_long:
            self.buy(size=1)

bt = Backtest(data, SmaCross, commission=.002,trade_on_close=True,cash=1000000,exclusive_orders=True)
stats = bt.run()
bt.plot()

stats = bt.optimize(fast=range(5, 100, 1),
                    slow=range(10, 100,1),
                    sig=range(5,200,1),
                    maximize='Equity Final [$]',
                    constraint=lambda param: param.fast < param.slow)

def rs(data):
    print(data)
    return RSIIndicator(pd.Series(data)).rsi()
class SmaCross(Strategy):
    l=20
    h=80
    def init(self):
        self.rsi = self.I(rs,self.data.Close)

    def next(self):
        if not self.position:
            if self.rsi < self.l:
                self.buy(size=1)
            else:
                self.sell(size=1)    
        
        if (self.rsi > self.h) and not self.position.is_short:
            
            self.sell(size=1)
        if (self.rsi < self.h) and not self.position.is_long:
            self.buy(size=1)

bt = Backtest(data, SmaCross, commission=.002,trade_on_close=True,cash=1000000,exclusive_orders=True)
stats = bt.run()
bt.plot(plot_return=True,plot_equity=True)