
# Web Automation Based api Algo Trading for Broaker Zerodha

This is python based library created for simple algo trading, It is developed using selenium. It helps for automatic data collection from [Zerotha Official Website](.https://kite.zerodha.com/)

These API can be user to place order in live market.

These api can be used to collect the data from website and save them in xml file and used for backtest.

* __Author: [Harpal](https://github.com/harpalnain)__
* These are unoffical api just created for fun.

### Prerequisites

Python 3.x

Also, you need the following modules:

* `selenium`
* `chromedriver`
* `websocket_client`
* `requests`
* `bs4`

You can clone this repo and install all preraquisites

## Getting started with API

### Overview
There are three public class `Zerodha`, `StockDataLogger` and `MarketSimulatore`. You can create instance of these class. For creating instance of `Zerodha` you need to pass Zeroda's credential as argument in constructor. `StockDataLogger` is used to save live data in xml files and `MarkerSimulator` class is used to backtest your stratergy using data saved in xml files.


### Getting Started

1. Create a dictonary contaning the credential and watch list no. that you want to subscibe for trading.
```python
creds = {	
          "trading":True,  
          "usr":"AB2111",
          "pswd":"Password@123",
          "pin":"124346",
          "trade_watchlist":1,
          "email":"lazypeople@gmail.com"
        }

```

2. Login and Subscibe: Create instance of Zerodha using credential.
ZC Call is used to define the Constant Value
* ZC.MODE_DEPTH_20 :- market depth 20 data
* ZC.MODE_DEPTH_5 :- market depth 5 data
* ZC.MODE_LTP :- Last Trading Price data
```python
from Brokers.Zerodha import ZC, ZerodhaConnect
z = ZerodhaConnect(usr=creds, headless = False)
#headless false means browser will open in backround
z.subscribe(time_interval = 1,mode = ZC.MODE_DEPTH_5)
```

3. Define a method where you implement your trading stratergy and register this methon with zerodha instance
```python
def on_ticks(ticks):
    print(ticks)
    #Add Stratergy Here 
z.on_ticks=on_ticks
```
 #### This tick data contains list of ticks in following example format.

```python    
    [{'timestamp': datetime.datetime(2021, 2, 14, 12, 26, 35), 'symbol': 'TCS', 'exchange': 'NSE', 'holdings': None, 'ltp': 3190.8, 'change': None, 'Prev. Close': '3206.00', 'Volume': 'NA', 'Avg. price': 'NA', 'LTQ': 'NA', 'LTT': '2021-02-12 15:58:42', 'Lower circuit': '2871.75', 'Upper circuit': '3509.85', 'total_bids': '0', 'total_offers': '0'}]
      
``` 
4. Place Order:-
```python
place_order(self,symbol = "IRCTC",
            exchange= 'NSE', 
            product = ZC.PRODUCT_TYPE_CNC,
            transaction_type =ZC.TRANSACTION_TYPE_BUY,
            order_type = ZC.ORDER_TYPE_MARKET,
            price = None, 
            qtn = 1 ):
```
### Following Constant are define in ZC Class for placing order
**_transaction_type_**  
* ZC.TRANSACTION_TYPE_BUY :- Buy Order
* ZC.TRANSACTION_TYPE_SELL :- Sell Order

**_product_**
* ZC.PRODUCT_TYPE_CNC :- "Cash and carry. Delivery based trades"
* ZC.PRODUCT_TYPE_MIS = "Intraday squareoff with extra leverage"

**_order_type_**

* ZC.ORDER_TYPE_MARKET = "Market Order"
* ZC.ORDER_TYPE_LIMIT = "Limit Order"


Price is kept none in case of market order and have some value in case of limit order.

5. Get Margins

```python
z.get_margin()

# This method return following example output format
{'equity': {'Available margin': 1465.21,
  'Used margin': 0.0,
  'Available cash': 1465.21,
  'Opening balance': 1465.21,
  'Payin': 0.0,
  'SPAN': 0.0,
  'Delivery margin': 0.0,
  'Exposure': 0.0,
  'Options premium': 0.0,
  'Collateral (Liquid funds)': 0.0,
  'Collateral (Equity)': 0.0,
  'Total collateral': 0.0},
 'commodity': {'Available margin': 0.01,
  'Used margin': 0.0,
  'Available cash': 0.01,
  'Opening balance': 0.01,
  'Payin': 0.0,
  'SPAN': 0.0,
  'Delivery margin': 0.0,
  'Exposure': 0.0,
  'Options premium': 0.0}}
```
6. Get Holdings 
```python
z.get_holdings()
#Return Folloing example output format
{'AVANTIFEED': {'Instrument': 'AVANTIFEED',
  'Qty.': '25',
  'Avg. cost': '483.34',
  'LTP': '499.15',
  'Cur. val': '12,478.75',
  'P&L': '395.20',
  'Net chg.': '+3.27%',
  'Day chg.': '-1.30%'},
 'BPCL EVENT': {'Instrument': 'BPCL EVENT',
  'Qty.': '15',
  'Avg. cost': '378.43',
  'LTP': '418.35',
  'Cur. val': '6,275.25',
  'P&L': '598.75',
  'Net chg.': '+10.55%',
  'Day chg.': '0.00%'}}
```
7. Save Data in xml file
```python
from Loggers.StockDataLogger import StockLogger
HsLogger = StockLogger(base_path ="path_for_data_to_be_saved",chunk_size = 100)
z.set_logger(hslogger=HsLogger)
```

8 Market Simulator:
Data Should be avalble for simulator that is saved by HsSimlator.
```python
from Brokers.MarketSimulator import TickSimulator
stocks =['SBICARD','TITAN','AARTIIND','IDEA', 'IRCTC','LT','SETFGOLD','PRINCEPIPE']
tick_sim = TickSimulator(time_interval = 1, usr = 'PAPER_TRADING')
tick_sim.subscribe(tickers = stocks, last_n_days = 60)
def on_ticks(ticks):
    print(ticks)
    #Add Stratergy Here 

tick_sim.on_ticks=on_ticks
```
Marker Simlator class will exactly behave real market only difference is that no real money and no real order will be place.This class not required broker accound but required data to be availble in xml format