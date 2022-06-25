from datetime import datetime

import backtrader as bt
from tqdm.auto import tqdm

pbar = tqdm(desc='Opt runs', leave=True, position=1, unit='run', colour='violet')
from tabnanny import verbose
import pandas as pd
data=pd.read_csv('/home/ubuntu/Downloads/nifty_10min_data.csv',parse_dates=True)
data=data.dropna()
from datetime import datetime
import backtrader as bt
import backtrader as bt
import numpy as np
from pandas import DataFrame



class MACD(bt.Strategy):
    params = (('fast_LBP', 12), ('slow_LBP', 26), ('max_position', 1), ('signal_LBP', 9))

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        from backtrader.indicators import SMA,EMA
        self.fast_EMA = EMA(self.data, period=self.params.fast_LBP)
        self.slow_EMA = EMA(self.data, period=self.params.slow_LBP)

        self.MACD = self.fast_EMA - self.slow_EMA
        self.Signal = EMA(self.MACD, period=self.params.signal_LBP)
        self.Crossing = bt.indicators.CrossOver(self.MACD, self.Signal, plotname='Buy_Sell_Line')
        self.Hist = self.MACD - self.Signal

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                #self.log('BUY EXECUTED, %.2f' % order.executed.price)
                pass
            elif order.issell():
                #self.log('SELL EXECUTED, %.2f' % order.executed.price)
                pass

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):

        # If MACD is above Signal line
        if self.Crossing > 0:
            if self.position.size < self.params.max_position:
                #self.close()
                self.buy()

        # If MACD is below Signal line
        elif self.Crossing < 0:
            if self.position.size > 0:
                self.close()
                #self.sell()


def bt_opt_callback(cb):
    pbar.update()


cerebro = bt.Cerebro()
#cerebro.addstrategy(MACD)
strats = cerebro.optstrategy(
        MACD,
    fast_LBP = range(10, 12),
    slow_LBP = range(10,12),
    #signal_LBP=range(1,100)
    )
#cerebro.addstrategy(strats)
df=data.copy()
#f['dt'] = pd.to_datetime(df['dt']).dt.tz_convert(None)
df['date'] = pd.to_datetime(df['date']).dt.tz_convert('Asia/Kolkata')
df.set_index('date', inplace=True)
df=df.dropna()
feed = bt.feeds.PandasData(dataname=df.dropna())
cerebro.adddata(feed)
import backtrader.analyzers as btanalyzers
cerebro.broker.setcommission(commission=0.000945)
#cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
#cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
#cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
#cerebro.addanalyzer(btanalyzers.Returns, _name="returns")
#cerebro.addanalyzer(btanalyzers.PyFolio,_name='portifolo')
cerebro.optcallback(cb=bt_opt_callback)
back=cerebro.run(stdstats=False,optreturn=True,optdatas=True)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
#cerebro.plot()
results =back
strats = [x[0] for x in results]  # flatten the result
for i, strat in enumerate(strats):
    rets = strat.analyzers.returns.get_analysis()
    print('Strat {} Name {}:\n  - analyzer: {}\n'.format(
        i, strat.__class__.__name__, rets))


