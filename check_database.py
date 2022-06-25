import os
from time import sleep
import datetime
import time
from common.message import message
os.system('rm database_started')
os.system('rm databasestart.txt')
open('database_started','w').write('False')
while True:
    os.system('screen -dmS database ipython3 accounts_database.py')
    print('screen -dmS database ipython3 accounts_database.py')
    while not ((0 <= time.localtime().tm_wday <= 4) and (datetime.datetime.strptime(
                            datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 09:15:01",
                            "%d-%m-%Y %H:%M:%S") <= datetime.datetime.now() <= datetime.datetime.strptime(
                        datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y") + " 15:30:00",
                        "%d-%m-%Y %H:%M:%S"))):  
        
        sleep(1)
        print('waiting market to open check_database.py')
    sleep(40)    
    started=False
    try:
        with open('databasestart.txt', 'r') as f:
            u=f.read()
    except:
        started=False
    if u=='True':
        started=True
    if started:
        open('database_started','w').write('True')
        message('started database successsfully')
        break
    if not started:
        os.system('screen -XS database quit')
        os.system('rm /home/ubuntu/pycharmprojects/tradeautomation/ticks.db')
        print('screen -XS database quit')
    else:
        sleep(5)
        print('Waiting for market to open...')        


