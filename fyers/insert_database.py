from fyers_api.Websocket import ws
from fyers.database import *
import time
import datetime
from fyers.script import name_to_script
import websocket
import logging
import pdb
from common import message as m
emergency_start=False
import time
emergency_do_not_stop=False
writing=False
c=0
with open('databasestart.txt', 'w') as f:
    f.write('False')
class database_ticks:#(name,fyers,token,cred_dict):
    def __init__(self, symbol, fyers):
        self.fyers=fyers
        self.symbol1=[]
        for i in symbol:
            self.symbol1.append(name_to_script(i))
        self.symbol=self.symbol1
        print(self.symbol)
        self.user_id = fyers.user_id
        self.password = fyers.password
        self.two_fa = fyers.two_fa
        self.redirect_url = fyers.redirect_url
        # redirect_url = 'http://127.0.0.1/
        self.app_id = fyers.app_id
        self.app_secret = fyers.app_secret
        self.access_token = fyers.app_id + ':' + fyers.token
        print(fyers.fyers.funds())
        # ["NSE:SBIN-EQ"]
        self.stock_name=self.symbol[0].split('-')[0].split(':')[1]
        create_tables([self.stock_name])


    def database(self):
        def custom_message(msg):
            #print(self.response)
            #print ("Custom " + str(self.response))
            #try:
            #print('hello bro ')
            global writing
            global c 
            if writing==False and c>5:
                if c<10:
                    open('databasestart.txt','w').write('True')
                writing=True
            if c<20:
                c+=1    
            #print(c)
            print(msg)
            insert_ticks(msg)
            #print(msg)
            #except Exception as error:
            #    print(error)    
        data_type = "symbolData"
        #ws.FyersSocket.websocket_data = custom_message
        #ws.websocket_data=custom_message
        #ws.websocket_data = custom_message
        fyersSocket = ws.FyersSocket(access_token=self.access_token,run_background=False,log_path="/home/ubuntu/pycharmprojects/tradeautomation/fyers")
        fyersSocket.websocket_data=custom_message
        waiting = True
        while 1==1:
            if datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:15:00","%d-%m-%Y %H:%M:%S") <= datetime.datetime.now() or emergency_start:
                print('subscribe')
                #pdb.set_trace()
                time.sleep(5)
                fyersSocket.subscribe(data_type=data_type,symbol=self.symbol)
                time.sleep(5)
                fyersSocket.keep_running()
                #break
        while True:
            if datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:30:00","%d-%m-%Y %H:%M:%S") <= datetime.datetime.now() :
                import sys
                sys.exit()
                print('hello')   
            # if (now.hour >= 15 and now.minute >= 30):
            #if ((0 <= time.localtime().tm_wday <= 4) and (datetime.datetime.strptime(
            #        datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 15:30:00",
            #       "%d-%m-%Y %H:%M:%S") <= datetime.datetime.now() <= datetime.datetime.strptime(
            #        datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 15:35:00",
            #        "%d-%m-%Y %H:%M:%S"))) or emergency_do_not_stop:
            #    #alice.unsubscribe(alice.get_instrument_by_symbol('NSE', name), LiveFeedType.COMPACT)
            #    import sys
            #    sys.exit()
        #db.close()
        #m.message('database closed ')
#database_ticks('ONGC')
