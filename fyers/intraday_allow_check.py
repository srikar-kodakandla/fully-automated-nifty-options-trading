import gspread
sa=gspread.service_account(filename='/home/ubuntu/google.json')
#sh=sa.open('Fyers - Scrips blocked for Intraday trading')
#sa.list_spreadsheet_files()
sh=sa.open_by_url('https://docs.google.com/spreadsheets/d/1ZCB9rhyTkGwGIAI8G5MO9fKcO8K_82TPaSlibQkVTzU/edit#gid=0')
#sh.sheet1.get()
import pandas as pd
data=pd.DataFrame(sh.sheet1.get())
blocked_stocks=data[0].tolist()
stocks=open('/home/ubuntu/pycharmprojects/tradeautomation/stock_selection.txt').read().split('\n')
allowed_stocks=[]
for i in stocks:
    if i.upper() in blocked_stocks:
        print(i)
    else:
        allowed_stocks.append(i)    
u=str()
for i in allowed_stocks:
    u+=str(i)
    u=u+'\n'
open('/home/ubuntu/pycharmprojects/tradeautomation/stock_selection.txt','w').write(u)
from common.message import message
message(f'Fyers allowed stocks for tomorrow trading : {allowed_stocks}')
print(*allowed_stocks,sep=',')