from common import message as m
from fyers.insert_database import database_ticks
import pandas as pd
import pickle
from time import sleep
import time
import pandas as pd
emergency_start=False
import datetime
a=True
sleep(20)
while a==True:
    try:
        intimate = open('intimate.txt', 'r')
        u=intimate.read().split('\n')[0]
        a=u
        if a==False:
            break
        print('Logged in ')
        intimate.close()
    except:
        print('Waiting for other python file to login ...')
        sleep(5)
wait=False 
while not wait: 
    wait=((0 <= time.localtime().tm_wday <= 4) and (datetime.datetime.strptime( 
            datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:14:58", 
            "%d-%m-%Y %H:%M:%S") <= datetime.datetime.now())) 
          
    if wait: 
        break 
    print('waiting market to open ')   
    if emergency_start: 
        break 
    #print('waiting') 
    sleep(1)
wait=True
try:
    h=pd.read_csv(('fyers/cred.csv'))
except :
    h = pd.read_csv(('cred.csv'))
accounts=[]
import time
import os
import pandas as pd
import sqlite3
from datetime import datetime
import sys
if os.getcwd()[0] == 'C':
    db = sqlite3.connect('ticks.db')
else:
    db = sqlite3.connect('ticks.db')
for i in h:
    with open(f'{i}', 'rb') as disk:
        accounts.append(pickle.load(disk))
name1=[]
for i in h:
    name1.append(i)
def accounts_database(name,accounts=accounts):
    sql = database_ticks(name,accounts[0])
    sql.database()
try:
    read=open('stock_selection.txt','r')
except: 
    read=open('fyers/stock_selection.txt','r')    
stock_name=read.read().split('\n')
read.close()
stock_name=stock_name[0]
#from fyers.broker_allow_stocks import allow
#allowed_stocks=allow(stock_name)
#stock_name=allowed_stocks[0]
count=0
while count<60:
    try:
        count+=1
        m.message("Ticks will save to database from now ")
        try:
            accounts_database([stock_name])
        except Exception as error:
            m.message(f"There may be an error in inserting to database ,{error}")
            sleep(10)
    except Exception as error :
        m.message(f"Final Call , it wont't try again , stopped inserting to database there may be an error in inserting to database , Ticks entering to database is stopped . Trades from will not work correctly , Algo trading won't work correctly , Please check code or contact srikar to solve issue , {error}")
        sleep(10)
