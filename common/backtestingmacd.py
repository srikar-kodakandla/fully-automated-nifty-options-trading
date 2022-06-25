from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
data=pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv',parse_dates=True)
data=data.dropna()
data=data.set_index('Date')
data.index=pd.to_datetime(data.index)
#data=data[-10000:]
import pandas as pd
from ta.trend import MACD
from tqdm import tqdm 

bar=tqdm(total=868725/4)

def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    print(n)
    return pd.Series(values).rolling(n).mean()
def ma(close,fast,slow,sig):
    global bar
    bar.update(1)
    close=pd.Series(close)
    return MACD(close=close,window_fast=fast,window_slow=slow,window_sign=sig).macd()
def ma1(close,fast,slow,sig):
    close=pd.Series(close)
    return MACD(close=close,window_fast=fast,window_slow=slow,window_sign=sig).macd_signal()
#SMA(data['Close'],10)      
class SmaCross(Strategy):
    fast=76
    slow=99
    sig=183
    def init(self):
        price = self.data.Close
        #self.ma1 = self.I(SMA, price, 50)
        #self.ma2 = self.I(SMA, price, 200)
        self.macd=self.I(ma,price,fast=self.fast,slow=self.slow,sig=self.sig)
        self.macd_sig=macd=self.I(ma1,price,fast=self.fast,slow=self.slow,sig=self.sig)

    def next(self):
        if crossover(self.macd, self.macd_sig):
            self.position.close()
            self.buy()
        elif crossover(self.macd_sig, self.macd):
            self.position.close()
            self.sell()


bt = Backtest(data, SmaCross, commission=0.002,trade_on_close=True,cash=1000000000000)
stats = bt.run()
bt.plot()

stats = bt.optimize(fast=range(5, 100, 1),
                    slow=range(10, 100,1),
                    sig=range(5,200,1),
                    maximize='Win Rate [%]',
                    constraint=lambda param: param.fast < param.slow)
