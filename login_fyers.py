login_fyers_or_not=False
login_fyers_or_not=False
from fyers.accounts_login import login_accounts
import re
from common.indicator import SuperTrend
import os 
#os.system('rm /home/ubuntu/pycharmprojects/tradeautomation/ticks.db')
from time import sleep, strftime
from termcolor import colored
import time
import numpy as np
from common import message as m
time.sleep(0.5)

import sys
from fyers.order import order
import datetime
from fyers.script import name_to_script
from fyers.quote import quote
from fyers.stoploss_percentage import percentage
from fyers.live import full_data
import pandas as pd
import os
import ta
import pickle
import datetime
now=datetime.datetime.now()
def login_fyers():
    global login_fyers_or_not
    while True:
        
        try:
            #stock_name='NSE:NIFTY50-INDEX'

            #accounts=login_accounts()
            try:
                h=pd.read_csv(('fyers/cred.csv'))
            except :
                h = pd.read_csv(('cred.csv'))
            accounts=[]    
            for i in h:
                with open(f'{i}', 'rb') as disk:
                    accounts.append(pickle.load(disk))
            intimate=open('intimate.txt','w')
            intimate.write('False')
            intimate.close()
            
            #data=l.full_data(stock_name)
            sleep(0.5)
            fyers=accounts[0].fyers
            login_fyers_or_not=True
            #fyers.funds()
            stock_name='NSE:NIFTY50-INDEX'
            l=full_data(accounts[0])
            data=l.full_data(stock_name,resolution=5,days=98)
            return accounts[0],fyers
            break
        except:
            try:
                os.system('rm /home/ubuntu/pycharmprojects/tradeautomation/ticks.db')
                pass
            except:
                pass
            m.message('Trying to Login Fyers account ...')
            import fyers.login_fyers
            login_fyers_or_not=False
            