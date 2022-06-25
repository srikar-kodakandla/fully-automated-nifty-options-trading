import time
import os
import pandas as pd
import sqlite3
from datetime import datetime
import sys 
#inserting_data_to_database=False
if os.getcwd()[0] == 'C':
    db = sqlite3.connect('ticks.db')
else:
    db = sqlite3.connect('ticks.db')
c = db.cursor()
from fyers.script import name_to_script
count1=0
u='False'
def get_hist(ticker, db=db,timeframe='1min'):
    global count1
    global u
    #token = instrumentLookup(instrument_df, ticker)
    try:
        opened=open('database_started','r').read()
    except:
        opened=False
    if opened=='True' and count1<6:
        count1+=1
        if os.getcwd()[0] == 'C':
            db = sqlite3.connect('ticks.db')
        else:
            db = sqlite3.connect('ticks.db')
        c = db.cursor()
    if opened!='True':
        opened=False
        count1=0
    if u=='False':     
        if os.getcwd()[0] == 'C':
            db = sqlite3.connect('ticks.db')
        else:
            db = sqlite3.connect('ticks.db')
        c = db.cursor()
        try:
            with open('databasestart.txt', 'r') as f:
                    u=f.read()
        except:
            u='False'            
    
    token=ticker.upper()
    ticker=name_to_script(token)
    token = ticker.split('-')[0].split(':')[1]
    data = pd.read_sql('''SELECT * FROM TOKEN%s WHERE ts >=  date() - '12 day';''' % token, con=db)
    data = data.set_index(['ts'])
    data.index = pd.to_datetime(data.index)
    ticks = data.loc[:, ['price']]
    df = ticks['price'].resample(timeframe).ohlc().dropna()
    return df

#from common.indicator import SuperTrend
#SuperTrend(data,80,3.6)