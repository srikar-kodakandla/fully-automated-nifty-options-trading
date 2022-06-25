from backtesting import Backtest, Strategy
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
data = pd.read_csv('/home/ubuntu/Downloads/5min_N50_10yr.csv', parse_dates=True)
#data=data[-60000:]
data = data.dropna()
data=data.set_index('Date')
data.index=pd.to_datetime(data.index)

import pandas as pd
from ta.trend import MACD


from backtesting.test import SMA


class SmaCross(Strategy):
    n1 = 116
    n2 = 814

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


bt = Backtest(data, SmaCross,
              cash=100000000, commission=.002,
              exclusive_orders=True)

#output = bt.run()



stats = bt.optimize(n1=range(2, 2000, 2),
    n2=range(2,2000,2),
    #h=range(1, 100, 5),
    maximize='Win Rate [%]', return_heatmap=True,constraint=lambda param: param.n1 < param.n2,max_tries=16000)
bt.plot()