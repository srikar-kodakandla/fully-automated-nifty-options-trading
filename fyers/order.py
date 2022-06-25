from fyers.login import login
from common import message as m
from fyers.script import name_to_script
from fyers.quote import quote
from fyers.stoploss_percentage import percentage
from math import floor
class order:
    def __init__(self,fyers):
        self.q = quote(fyers)
        self.fyers=fyers.fyers
        self.tokens_list = []
    def position_symbol(self):
        sym={}
        id={}
        for i in self.fyers.positions()['netPositions']:
            if i['netQty']!=0 :
                sym.update({i['symbol']:i['side']})
                id.update({i['symbol']:i['id']})
        return sym,id

    def position_id(self):
        pos=[]
        sym=self.position_symbol()
        for i in self.fyers.orderbook()['orderBook']:
            for j in sym:
                if i['symbol']==j:
                    pos.append(i['orderNumStatus'])
        return pos

    def predict_order_id(self):
        posi=[]
        for i in self.position_id():
            a=i.split(':')
            b=a[0].split('-')
            c[-1]=b[-1]
            posi.append(''.join(c))
        return posi

    def buy_co(self,name,stoploss=0,buy_sell=1):
        name=name_to_script(name)
        data = {
        "symbol" : name,
        "qty" : 1,
        "type" : 2,
        "side" : buy_sell,
        "productType" : "CO",
        "limitPrice" : 0,
        "stopPrice" : 0,
        "disclosedQty" : 0,
        "validity" : "DAY",
        "offlineOrder" : "False",
        "stopLoss" : stoploss,
        "takeProfit" : 0
        }
        value=self.tokens_list.append(self.fyers.place_order(data))
        print(self.tokens_list[-1])
        trade_message=self.tokens_list[-1]['message']
        if buy_sell ==-1:
            m.message(f'Traded (sold)  {name}  :{trade_message}')
        if buy_sell==1:
            m.message(f'Traded (Brought) {name} : {trade_message}')
        return value

    def sell_co(self,name):
        id=self.position_id()[2]
        ii=self.fyers.cancel_order(
        data = {
        "id" : id,
        "type" : "2"
        }
        )
        m.message(f"{name}order tried to exit : {ii['message']}")
    def sell(self,name):
        name_script=name_to_script(name)
        symbol=self.position_symbol()[1][name_script]
        data = {
            "id": symbol
        }
        ii=self.fyers.exit_positions(data)
        m.message(f"{name} order tried to exit : {ii['message']}")
    def buy(self,name,qty=1,buy_sell=1):
        name_script=name_to_script(name)
        data = {
            "symbol": name_script,
            "qty": qty,
            "type": 2,
            "side": buy_sell,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss":0,
            "takeProfit": 0
        }
        ii=self.fyers.place_order(data)
        value = self.tokens_list.append(ii)
        print(self.tokens_list[-1])
        trade_message = self.tokens_list[-1]['message']
        if buy_sell == -1:
            m.message(f'Traded (sold) {name} ,quantity : {qty} : {trade_message}')
        if buy_sell == 1:
            m.message(f'Traded (Brought) {name} , quantity : {qty} : {trade_message}')

    def no_of_stocks(self,name,percent=100,margin=5):
        name=name_to_script(name)
        ltp=self.q.quote(name)
        f=(self.fyers.funds()['fund_limit'][0]['equityAmount'])
        p=percentage(f, percent)
        return floor((p*margin)/ltp)



