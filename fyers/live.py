import time
"""I need to check the time of the database data and fyers data before concatinating , if not same or time is repeated then i needed
to do certain things to over come the problem """
import os
import pandas as pd
import sqlite3
from datetime import datetime
import sys
if os.getcwd()[0] == 'C':
    db = sqlite3.connect('ticks.db')
else:
    db = sqlite3.connect('ticks.db')
c = db.cursor()
try:
    os.system('sudo chown root ticks.db')
    os.system('sudo chown ubuntu ticks.db')
except:
    pass
from fyers.history import history
from fyers.look_database import get_hist
#data=get_hist('reliance')
#db.execute('select * from TOKENNIFTY50')
class full_data:
    def __init__(self,fyers):
        self.fyers=fyers
        self.a = history(self.fyers)
    def full_data(self,name,days=5,resolution="1",date_format="1",range_from=None,range_to=None,cont_flag="1"):
        try:
            y=True
            data=get_hist(name,timeframe=str(resolution)+'min')
        except:
            y=False
            print('The given stock is not there in database ! ')

        data1=self.a.history(name,days,resolution,date_format,range_from,range_to,cont_flag)
        data1=pd.DataFrame(data1['candles'], columns=['ts', 'open', 'high', 'low', 'close', 'volume']).set_index('ts').drop(['volume'], axis=1)
        data1.index = pd.to_datetime(data1.index, unit='s').tz_localize('Africa/Abidjan').tz_convert('Asia/Kolkata')
        if y:
            #import pdb
            #pdb.set_trace()
            #data=pd.DataFrame(data['candles'], columns=['ts', 'open', 'high', 'low', 'close', 'volume']).set_index('ts').drop(['volume'], axis=1)
            data.index=pd.to_datetime(data.index, unit='s').tz_localize('Asia/Kolkata').tz_convert('Asia/Kolkata')
            final=pd.concat([data1,data])
            final=final.reset_index().drop_duplicates(subset='ts').set_index('ts')
        else:
            final=data1
        return final

