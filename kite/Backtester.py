#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:43:15 2020

@author: harpal
"""

from whatappAtom import WhatsApp
from MarketSimulator import TickSimulator
from signal import signal, SIGINT
from sys import exit
import threading
import time
import json
import datetime as dt
import pandas as pd
import numpy as np
from Strategies import StocksNStratergy

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

def handler(signal_received, frame):
    # Handle any cleanup here
    tick_sim.stop()
   
#signal(SIGINT, handler)

timeStamp =dt.datetime.now().replace(microsecond=0)
stocks =['TITAN','BAJAJFINSV']
#stocks =['SBICARD','TITAN','AARTIIND','IDEA', 'IRCTC','LT','SETFGOLD','PRINCEPIPE']
tick_sim = TickSimulator(time_interval = 0.01, usr = 'SIMU1')
tick_sim.subscribe(tickers = stocks, last_n_days = 60)
stg = StocksNStratergy(broker = tick_sim)
tick_sim.init_trade_setup(stg)

print('start',today)
#tick_sim.on_ticks = on_ticks    
tick_sim.start()
tick_sim.join()
today = dt.datetime.today()
print('stop',today)
'''
tick_sim.start()


tick_sim.stop()

#tick_sim.join()




'''
today = dt.datetime.today()
market_start_time = dt.datetime.combine(today, dt.time(9, 15, 0))
market_stop_time = dt.datetime.combine(today, dt.time(15, 29, 59))

print('start',today)
#tick_sim.on_ticks = on_ticks    
#tick_sim.start()
tick_sim.join()
today = dt.datetime.today()
print('stop',today)
'''
   
