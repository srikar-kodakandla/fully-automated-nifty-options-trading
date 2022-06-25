#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:50:26 2020

@author: harpal
"""

import json
import time
import os
from Brokers.Zerodha import ZC
import datetime as dt
import pandas as pd
#from HPlots import Hplotter
import math
class AdDict(dict):
    def __setattr__(self, key, value):
        self[key]=value

    def __getattr__(self, item):
        return self.get(item)
    
class Stock:

    #broker = None  
    def __init__(self, exchange, symbol, broker):
        self.broker = broker
        self.log_path = "logs/"
        self.setup_path = self.broker.user_name + '/'
        self.state = AdDict()
        
        
        #Get Stats Data from log files
        self.exchange = exchange
        self.symbol = symbol
        self.file_name = exchange + '_' + symbol
        f_name =self.setup_path+ self.file_name + ".json"
        if os.path.exists(f_name):
            with open(f_name, 'rb') as input:
                self.state.update(json.load(input))
                self.stats= AdDict()
                self.stats.update(self.state['stats'])
                self.state['stats'] = self.stats
                #print(self.state)
        else: 
            self.state.charting = False
            self.state.stats = self.stats= AdDict()
            self.stats.equity_margin = None
            self.stats.budget = 50000
            self.stats.lot_value = 5000
            self.stats.holdings = 0
            self.stats.profit = 0
            self.stats.invested = 0
            self.stats.trades_count = 0
            self.stats.avg_price = 0
            self.stats.ltp = None
            self.state.buy_stack = [] #Format:- {'price':1000,'qtn':10}
            self.state.sell_stack = [] #Format:- {'price':1000,'qtn':10}
            self.state.active_stratergy = 'SimpleRenko'
        self.ltp = self.stats.ltp
        self.margin=self.stats.equity_margin
        self.update_margins()
        
    def update_margins(self):
        try:
            time.sleep(1)
            margins = self.broker.get_margins()
            print('Margins', margins)
            self.margin  =  margins['equity']['Available margin']
            print('Margin:', self.margin)
        except:
            print('Get Margin Failed')
        
    def square_off_buy_trade(self, trade):
        #price = trade['price'] 
        qtn = trade['qtn']        
        self.place_sell_order(qtn = qtn)
        pro = (self.ltp - trade['price']) * qtn
        self.stats.profit += pro
        self.stats.trades_count+=1
        self.state.buy_stack.remove(trade)
        msg = self.exchange+ '-' + self.symbol +str(self.ltp) + " Sell Qty "+str(qtn) + 'profit:' + str(pro)
        subject = self.broker.user_name + ' sell order placed'
        #self.broker.mailer.mail(subject=subject, text=msg)
        print(subject + msg)
        
        
    def square_off_sell_trade(self,trade):
        qtn = trade['qtn']    
        self.place_buy_order(qtn = qtn)
        self.state.sell_stack.remove(trade)
        #self.state.buy_stack.append(trade)

                
    def chart_it(self, data):
        if self.state.charting:
            pass
            #self.plotter = Hplotter(self.exchange, self.symbol, data)
            #self.plotter.start()

    #TODO pass parameters              
    def place_buy_order(self, qtn = None):
        if qtn is None:
            qtn = math.floor(self.stats.lot_value/self.ltp)
        if qtn > 0:
            self.broker.place_order(exchange = self.exchange, symbol = self.symbol,
                                    price = self.ltp, qtn=qtn)
            self.update_margins()
            self.stats.invested += self.ltp * qtn
        self.state.buy_stack.append({'price':self.ltp,'qtn':qtn})
        msg = self.exchange + '-' + self.symbol +str(self.ltp) + " Buy Qty "+str(qtn)
        subject = self.broker.user_name + ' buy order placed'
        #self.broker.mailer.mail(subject=subject, text=msg)
        print(subject + msg)
        

    #TODO pass parameters
    def place_sell_order(self, qtn = 1):
        if qtn > 0:
            self.broker.place_order(exchange = self.exchange, symbol = self.symbol,
                                    transaction_type =ZC.TRANSACTION_TYPE_SELL,
                                    price = self.ltp, qtn = qtn)   
            self.update_margins()
            self.stats.invested -= self.ltp * qtn
        self.state.sell_stack.append({'price':self.ltp,'qtn':qtn})

        
       
    def save(self):  
        self.stats.ltp = self.ltp
        self.stats.equity_margin = self.margin
        if self.state.charting:
            self.plotter.stop()
        f_name =self.setup_path+ self.file_name + ".json"
        if not os.path.exists(self.setup_path):
            os.makedirs(self.setup_path)
            
        with open(f_name, 'w') as output:
            #print(self.state)
            json.dump(self.state, output, indent=4)
            
    #def __del__(self):
    #    self.save()
    
'''
    def place_order(self,symbol = None,
                    exchange= None, 
                    product = ZC.PRODUCT_TYPE_CNC,
                    transaction_type =ZC.TRANSACTION_TYPE_BUY,
                    order_type = ZC.ORDER_TYPE_MARKET,
                    price = None, 
                    qtn = 1 ):
''' 
               
    
