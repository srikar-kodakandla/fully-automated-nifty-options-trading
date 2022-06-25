creds = {	
    "trading":True,  
    "usr":"KI3644",
    "pswd":"Nanna143!",
    "pin":"825556",
    "trade_watchlist":7,
    "email":"kodakandlasrikar99@gmail.com"
    }
import warnings
warnings.filterwarnings("ignore")
#from click import option
from kite.Brokers.Zerodha import *
z = ZerodhaConnect(usr=creds, headless = False)
driver= z.subscribe()
z.delete_all_kite()
driver= z.subscribe()
z.get_subscribed_ticker()
funds=z.get_margins()['equity']['Available margin']
def find(path):
    return driver.find_element_by_xpath(path)
z.
def open_order():
    try:
        a=dict()
        j=1
        for i in range(1,100000):
            t=driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[1]/div/div/table/tbody/tr[{i}]/td[3]/span[1]/span').text
                                    #find('/html/body/div[1]/div[2]/div[2]/div[2]/div/section[2]/div/div/table/tbody/tr[2]/td[3]/span[1]/span').text
            a[t]=dict()
            a[t]['time']=find(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr[{i}]/td[2]/span').text
            a[t]['type']=find(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr[{i}]/td[3]/span').text
            a[t]['nrml']=driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr[{i}]/td[5]').text
            a[t]['qty']=find(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr{i}/td[6]').text
            a[t]['ltp']=find(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr{i}/td[7]/span').text
            a[t]['price']=find(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr{i}/td[8]/span').text
            a[t]['status']=find(f'/html/body/div[1]/div[2]/div[2]/div[2]/div/section[{j}]/div/div/table/tbody/tr{i}/td[9]/span[1]/span').text
        return a
    except:
        try:
            return a 
        except:
            return False
    
def executed_order():
    find('/html/body/div[1]/div[2]/div[2]/div[2]/div/section[2]/div/div/table/tbody/tr[1]/td[3]/span[1]/span')
    find('/html/body/div[1]/div[2]/div[2]/div[2]/div/section[1]/div/div/table/tbody/tr[1]/td[3]/span[1]/span')
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/a[2]/span').click()
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section[1]/div/div/table/tbody/tr[1]/td[3]/span[1]/span').text

driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/section[2]').text




from nsepy import get_history
from datetime import date
data = get_history(symbol="SBIN", start=date(2015,1,1), end=date(2015,1,31),)
data[['Close']].plot()