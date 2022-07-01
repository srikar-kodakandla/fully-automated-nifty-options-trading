#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime as dt
import pdb
import re
try:
    import background
except:
    import os
    os.system('pip install background')  
    import background
import threading
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
#from selenium.common.exceptions import NoSuchElementException 
import pandas as pd
from io import StringIO 
from bs4 import BeautifulSoup
import sys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
class None_Web_Eelement:
    __instance = None
    def __init__(self):
        if None_Web_Eelement.__instance != None:
            raise Exception("Sigleton Class")
        else:
            self.text = None
            None_Web_Eelement.__instance = self
    def __bool__(self):
        return False
    def getInstance():
        """ Static access method. """
        if None_Web_Eelement.__instance == None:
            None_Web_Eelement()
        return None_Web_Eelement.__instance
    def click(self):
        print('Element:Not Found')
        
    def find_element_by_xpath(self,text):
        print('Parent Element of :'+ text +' Not Found')
        return self
    
class ZC:
    MAX_NO_WATCHLIST = 5
    # Available tick subscribtion modes.
    MODE_DEPTH_20 = "depth_20"
    MODE_DEPTH_5 = "depth_5"
    MODE_LTP = "ltp"
    
    #Order Parameter
    TRANSACTION_TYPE_BUY = "Buy (B)"
    TRANSACTION_TYPE_SELL = "Sell (S)"
    PRODUCT_TYPE_CNC = "Cash and carry. Delivery based trades"
    PRODUCT_TYPE_MIS = "Intraday squareoff with extra leverage"
    ORDER_TYPE_MARKET = "Market"
    ORDER_TYPE_LIMIT = "Limit"
    
    
    #Page reference
    login_url = "https://kite.zerodha.com/"
    xpath_username = "//*[@id='container']/div/div/div/form/div[2]/input"
    xpath_pswd = "//*[@id='container']/div/div/div/form/div[3]/input"
    xpath_pin = "//*[@id='container']/div/div/div/form/div[2]/div/input"
           
class ZerodhaConnect(threading.Thread):
    close_time = dt.datetime.now().replace(hour=15, minute=29, second=55, microsecond=0)
    open_time = dt.datetime.now().replace(hour=9, minute=15, second=00, microsecond=0)
    start_time = dt.datetime.now().replace(hour=9, minute=00, second=00, microsecond=0)
    def __init__(self,usr = None, headless = True):
        pswd=usr['pswd'] 
        pin = usr['pin']
        self.user_name = usr['usr'] 
        self.wlist = usr['trade_watchlist']
        self.mail = usr['email']
        
        #chrome_options = chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--disable-notifications")
        #if headless:
        #    chrome_options.add_argument("--window-size=1920,1080")
        #    chrome_options.add_argument("--disable-extensions")
        #    chrome_options.add_argument("--proxy-server='direct://'")
        #    chrome_options.add_argument("--proxy-bypass-list=*")
        #    chrome_options.add_argument("--start-maximized")
        #    chrome_options.add_argument('--headless')
        #    chrome_options.add_argument('--disable-gpu')
        #    chrome_options.add_argument('--disable-dev-shm-usage')
        #    chrome_options.add_argument('--no-sandbox')
        #    chrome_options.add_argument('--ignore-certificate-errors')
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        
        #self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        options = Options()
        if headless:
            options.headless = True
        self.driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
        
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        
        self.subscribed_stocks = []  
        self.logger = None
        self.ticker_element = None
        #Init valriables
        
        self.driver.get(ZC.login_url)
        self.driver.maximize_window()
       
        ''' Login Procedure '''
        try:
            if self.user_name:        
                self.driver.find_element_by_xpath(ZC.xpath_username).send_keys(self.user_name)
                self.driver.find_element_by_xpath(ZC.xpath_pswd).send_keys(pswd+Keys.ENTER)
                time.sleep(1)
                self.driver.find_element_by_xpath(ZC.xpath_pin).send_keys(pin+Keys.ENTER)
            else:
                self.wait_for_login()
        except:
            print('Login Failed')
            exit(0)
            
        ''' Left Container elements '''
        time.sleep(5)
        
        self.el_left_container = self.driver.find_element_by_class_name('container-left')
        self.el_watchlist_selector = self.el_left_container.find_element_by_class_name('marketwatch-selector')
        self.wachlists = self.el_watchlist_selector.find_elements_by_tag_name('li')
        self.mode =  ZC.MODE_LTP # default mode

        # Callbacks
        self.on_ticks = None
        
        self.sleep_time = 1
        self.stop_flag = False
        self.stratergy = False
        self.hslogger = False
        self.mailer = False
    def set_logger(self,  hslogger = None):
        self.hslogger = hslogger
        
    def set_mailer(self, mailer = None):
        self.mailer = mailer

      
    def stop(self):       
        if self.stratergy:
                self.stratergy.save()
        self.stop_flag = True

    def wait_for_login(self):
        while True:
            time.sleep(5)
            if "dashboard" in self.driver.current_url:
                break;
        print('Login Successfully')
        
    def get_subscribed_ticker(self):
        return self.subscribed_stocks
            
    def subscribe(self,time_interval = 5,mode='ltp'):
        if self.wlist < 1 or self.wlist > 7:
            raise Exception('Invalid wlist_index should be in range of 1 to 5')

        self.wachlists[self.wlist-1].click()
        self.time_interval = time_interval
        open_watchlist =  self.el_left_container.find_element_by_class_name("vddl-list")
        el_all_ins = open_watchlist.find_elements_by_class_name("instrument")
        self.instruments_count = len(el_all_ins)
        self.mode = mode
        ticker_map = {'NSE':{},'BSE':{}, 'NFO':{}}
        for el in el_all_ins:
            symbol =  ZerodhaConnect.find_el_by_class_name(el,'nice-name').text
            #print(symbol)
            exchange =  ZerodhaConnect.find_el_by_class_name(el,'exchange').text
            #print(exchange)
            if exchange is None:
                exchange = 'NSE'
            self.subscribed_stocks.append({'exchange':exchange,'symbol':symbol})
            ticker_map[exchange][symbol] = el
            #pdb.set_trace()
            
        self.ticker_element = ticker_map
        if self.mode == ZC.MODE_DEPTH_5 or mode == ZC.MODE_DEPTH_20:
            for el in el_all_ins:
                time.sleep(1)
                self.driver.execute_script("arguments[0].scrollIntoView();", el)
                hover = ActionChains(self.driver).move_to_element(el)
                hover.perform()
                
                time.sleep(0.3)
                action = ZerodhaConnect.find_el_by_class_name(el,'actions')
                action.find_element_by_xpath("//span[@data-balloon='Market Depth (D)']").click()
                #continue
                if mode == ZC.MODE_DEPTH_20:
                    time.sleep(1)
                    try:
                        dp_toggle = ZerodhaConnect.find_el_by_class_name(el,'depth-toggle')
                        self.driver.execute_script("arguments[0].scrollIntoView();", dp_toggle)
                        dp_toggle.click()
                    except Exception:
                        print('Depth 20 Error')
        return self.driver  
    def add_kite(self,stock_name):
      stock_nam=re.sub('w','',re.sub('th','',stock_name))
      #pdb.set_trace()
      self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div/input').send_keys(stock_nam)
      name_kite=self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/div/li/span[1]/span').text
      el=self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/ul/div/li[1]')
      hover = ActionChains(self.driver).move_to_element(el)
      hover.perform()
      sleep(0.5)
      hover.click_and_hold()
      
      self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/ul/div/li[1]/span[3]/button[5]').click()
      self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div/input').send_keys(Keys.ESCAPE)
      #self.subscribe()

    def delete_first_kite(self):

        def sam():
            hover = ActionChains(self.driver).move_to_element(el)
            hover.perform()
            hover.click_and_hold()
            action = el.find_element_by_class_name('actions')
            action.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[2]/div/div[1]/div/span/span[5]').click()
        try:
            el=self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[2]/div/div[1]')
            sam()
        except:
            try:
                el=self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div/div/span[1]/span/span')
                sam()
            except:
                el=self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div') 
                sam()
        #hover = ActionChains(self.driver).move_to_element(el)
        #hover.perform()
        #hover.click_and_hold()
        #action = el.find_element_by_class_name('actions')
        #action.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[2]/div/div[1]/div/span/span[5]').click()
    def delete_all_kite(self):
      #self.add_kite('RELIANCE')
      #self.add
      for i in range(55):
        try:
          self.delete_first_kite()
        except Exception as e:
          print(e)
          break
    #delete_all_kite()

    def place_order(self,symbol = None,
                    exchange= 'NSE', 
                    product = ZC.PRODUCT_TYPE_CNC,
                    transaction_type =ZC.TRANSACTION_TYPE_BUY,
                    MARKET=True,
                    order_type = ZC.ORDER_TYPE_MARKET,
                    price = None, 
                    qtn = 1 ):
        try:
            self.driver.find_element_by_xpath('/html/body/div[2]/div[6]/div').click()
        except:
            pass
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/form/section/footer/div[2]/button[2]').click()
        except:
            pass    
        try:
            self.delete_all_kite()
        except:
            pass    
        try:
            #print('Ticker element is : ')
            #print(ticker_element)
            print(1/0)
            self.delete_all_kite()
            self.subscribe()
            el = self.ticker_element[exchange][symbol]
        except Exception as error:
            #print(error)
            #self.delete_all_kite()
            self.add_kite(symbol)
            self.subscribe()
            el = self.ticker_element[exchange][symbol]
            #pdb.set_trace()
            #self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div/input').send_keys(symbol)
            #el=self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/ul/div/li[1]')

            print('Element not found for order so searched in given column')
            #return False
        
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", el)
            hover = ActionChains(self.driver).move_to_element(el)
            hover.perform()
            action = el.find_element_by_class_name('actions')       
            action.find_element_by_xpath("//span[@data-balloon='"+transaction_type+"']").click()
            order_window = self.driver.find_element_by_class_name("order-window")
            # Default order Type in Zerodha is Market
            #time.sleep(0.1)
            if product == ZC.PRODUCT_TYPE_MIS:
                order_window.find_element_by_xpath("//div[@data-balloon='"+product+"']").click()
            if MARKET==True:
                self.driver.find_element_by_xpath('//*[@id="app"]/form/section/div[2]/div[2]/div[2]/div[2]/div/div[1]/label').click()
            if order_type == ZC.ORDER_TYPE_LIMIT:   
                order_type = order_window.find_element_by_xpath("//div[@data-balloon='"+ order_type+"']")
                order_type.click()
                price_form = order_window.find_element_by_xpath("//input[@label='Price']") 
                price_form.clear()
                price_form.clear()
                if price is None:
                    return False
                price_form.send_keys(str(price))

            order_qtn = order_window.find_element_by_xpath("//input[@label='Qty.']")
            print(order_qtn.text)
            order_qtn.clear()
            order_qtn.send_keys(str(qtn) + Keys.ENTER)
            sleep(1)
            order_status=self.driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div/div').text
            print(order_status)
            
            if 'is placed.' in order_status:
                if 'Check the orderbook for status.' in order_status:
                    try:
                        self.delete_all_kite()
                    except:
                        pass
                    return True
                else:
                    if 'is complete.' in order_status:
                        try:
                            self.delete_all_kite()
                        except:
                            pass
                        return True
                    else:
                        jj=False
                        #return False   
            else:
                if 'is complete.' in order_status:
                        try:
                            self.delete_all_kite()
                        except:
                            pass
                        return True
                else:
                    jj=False
                    #return False  
            if not jj:
                try:
                    self.driver.find_element_by_xpath('/html/body/div[1]/form/section/footer/div[2]/button[2]').click()
                    try:
                        self.delete_all_kite()
                    except:
                        pass
                    return False
                except:
                    try:
                        self.delete_all_kite()
                    except:
                        pass
                    return False              
        except Exception as e:
            print('Order Error:', e)
            try:
                self.delete_all_kite()
            except:
                pass
            return False
        
    @background.task
    def run(self):
        time.sleep(1)
        while True:
            if self.stop_flag:
                break
            if self.on_ticks:
                try:
                    #start_time = int(round(time.time() * 1000))
                    start_time = time.time()
                    timeStamp =dt.datetime.now().replace(microsecond=0)           

                    src_code = self.el_left_container.get_attribute('innerHTML')
                    soup =  BeautifulSoup(src_code,'lxml')

                    instruments = soup.find_all('div', class_='instrument')
                    active_list = int(self.get_soup_text(soup,'li','item selected'))

                    if self.wlist != active_list or self.instruments_count != len(instruments):
                        print('change on browser')
                        self.subscribe(wlist_index= active_list,mode=self.mode,time_interval=self.time_interval)
                        continue
                #Get Tick Data
                    ticks = self.get_ticks_data(instruments,timeStamp)
                    self.on_ticks(ticks)
                    escaped_time = time.time() -  start_time

                    if escaped_time < self.time_interval:
                        time.sleep(self.time_interval - escaped_time)
                except Exception as e:
                    print('Distrubed ' +e)
                    time.sleep(10)

                
    def get_ticks_data(self,instruments, timeStamp):
        ticks = []
        for el in instruments:
            tickdata = {}
            tickdata['timestamp'] = timeStamp
            tickdata['symbol'] = self.get_soup_text(el,'span','nice-name')
            exchange = self.get_soup_text(el,'span','exchange')
            if exchange is None:
                exchange = 'NSE'
            tickdata['exchange']=exchange
            tickdata['holdings'] =  self.get_soup_text(el,'span','holding-quantities')
            tickdata['ltp'] =  float(self.get_soup_text(el,'span','last-price'))
            tickdata['change'] =  self.get_soup_text(el,'span','change-percent')
            
            mk_dp = el.find('div', class_='market-depth')
            if mk_dp:
                #Get OHLC Data
                ohlc_table = mk_dp.find('div', class_='ohlc').find_all('div', class_='six columns')
                for data in ohlc_table:
                    if data.label.text not in ['Open', 'High', 'Close', 'Low']:
                        tickdata[data.label.text] = data.span.text
                    
                #Get Bids Table
                bids_table = el.find('table', class_='six columns buy')
                #bids_pd = pd.DataFrame(columns = ['bid', 'orders', 'qty'])
                #self.get_table_in_pd(bids_pd,bids_table)
                total_bids = self.get_soup_text(bids_table.tfoot,'td','text-right')
                #tickdata['bid_table'] = bids_pd
                tickdata['total_bids'] = total_bids
                    
                #Get Offers Table
                offer_table = el.find('table', class_='six columns sell')
                #offer_pd = pd.DataFrame(columns = ['bid', 'orders', 'qty'])
                #self.get_table_in_pd(offer_pd,offer_table)
                total_offers = self.get_soup_text(offer_table.tfoot,'td','text-right')
                #tickdata['offer_table'] = offer_pd
                tickdata['total_offers'] = total_offers 
            ticks.append(tickdata)
        return ticks
        
    def get_margins(self):
        self.driver.find_element_by_partial_link_text('Funds').click()
        time.sleep(0.1)
        container =  self.driver.find_element_by_class_name('container-right')
        html_src = container.get_attribute('innerHTML')
        soup =  BeautifulSoup(html_src,'lxml')
        rows = soup.find_all('div', class_='six columns')
        
        margins = {}
        for row in rows:
            data = margins[next(row.h3.stripped_strings)] = {}
            table = row.find('table', class_="table")
            items = table.find_all('tr')
            for item in items:
                tds = item.find_all('td')
                key = tds[0].text.strip().split(' \n')[0]               
                data[key] =float(tds[1].text.strip().replace(',',''))
        return margins
    
    def get_holdings(self):
        self.driver.find_element_by_partial_link_text('Holdings').click()
        time.sleep(0.1)
        container =  self.driver.find_element_by_class_name('container-right')
        html_src = container.get_attribute('innerHTML')
        
        keys = []
        Holdings = {}
        soup =  BeautifulSoup(html_src,'lxml')
        table = soup.find('table')        
        heads = table.thead.tr.find_all('th')
        for item in heads:
            keys.append(item.text.strip())
            
        data_items =table.tbody.find_all('tr')
            
        for tds in data_items:
            values = tds.find_all('td')
            holding = {}
            symbol = values[0].text.strip()
            for i in range(len(values)):
                holding[keys[i]] =values[i].text.strip()
                Holdings[symbol] = holding
                
        return Holdings 
    
    def exit_all_positions(self):
      self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[1]/a[4]/span').click()
      time.sleep(0.1)
      self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/thead/tr/th[1]/div/label/span').click()
      self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tfoot/tr/td[1]/button').click()
      self.driver.find_element_by_xpath('//*[@id="app"]/div[5]/div/div/div/div[3]/div/div/button[1]').click()
    
    def get_position(self):
        position=dict()
        self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[1]/a[4]/span').click()
        time.sleep(0.1)
        try:
          for i in range(1,100):
            instrument=self.driver.find_element_by_xpath(f'//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tbody/tr[{i}]/td[3]/span[1]').text
            position[instrument]={}
            position[instrument]['product']=self.driver.find_element_by_xpath(f'//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tbody/tr[{i}]/td[2]').text
            position[instrument]['qty']=self.driver.find_element_by_xpath(f'//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tbody/tr[{i}]/td[4]').text
            position[instrument]['avg']=self.driver.find_element_by_xpath(f'//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tbody/tr[{i}]/td[5]').text
            position[instrument]['ltp']=self.driver.find_element_by_xpath(f'//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tbody/tr[{i}]/td[6]').text
            position[instrument]['pandl']=self.driver.find_element_by_xpath(f'//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tbody/tr[{i}]/td[7]').text
        except:
          pass
        try:
          totalpandl=self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/section[1]/div/div/table/tfoot/tr/td[4]').text
        except:
          totalpandl=0
        position['totalpandl']=totalpandl
        return position  

    def get_positions(self):
        self.driver.find_element_by_partial_link_text('Positions').click()
        time.sleep(0.1)
        container =  self.driver.find_element_by_class_name('container-right')
        html_src = container.get_attribute('innerHTML')
        
        keys = []
        Holdings = {}
        soup =  BeautifulSoup(html_src,'lxml')
        table = soup.find('table')        
        heads = table.thead.tr.find_all('th')
        for item in heads:
            keys.append(item.text.strip())
            
        data_items =table.tbody.find_all('tr')
            
        for tds in data_items:
            values = tds.find_all('td')
            holding = {}
            symbol = values[0].text.strip()
            for i in range(len(values)):
                holding[keys[i]] =values[i].text.strip()
                Holdings[symbol] = holding
                
        return Holdings 
    @staticmethod
    def get_table_in_pd(pd_table,el_table):
        rows = el_table.tbody.find_all('tr')
        for i in range(len(rows)):
            row = rows[i]
            row_data = []
            tds = row.find_all('td')
            for data in tds:
                row_data.append(data.text.strip())
            pd_table.loc[i] = row_data
        
    @staticmethod
    def get_soup_text(soup:BeautifulSoup=None, tag=None, class_name=None):
        item = soup.find(tag, class_ = class_name)
        if item:
            try:
                data = item.text.strip()
                return data
            except Exception:
                return item.text 
        return None
        
    @staticmethod
    def find_el_by_class_name(el,class_name):
        try:
            return el.find_element_by_class_name(class_name)
        except Exception:
            return None_Web_Eelement.getInstance()
     
    def init_trade_setup(self,stratergy):
        self.stratergy = stratergy
        self.on_ticks = self._after_market_tick_consumer
        
    def _tick_consumer(self,ticks):
        #print(ticks[0])
        if self.hslogger:
            self.hslogger.log_ticks(ticks)
            
        self.stratergy.actions(ticks) 
        
        now = dt.datetime.now()
        #print('\r'+str(now), sep='')
        sys.stdout.write( self.user_name + str(now) + "\r")
        #sys.stdout.write(str(ticks[0]) + "\r")
        if now > ZerodhaConnect.close_time:
            self.stop()
                
    def _after_market_tick_consumer(self,ticks):
        print(ticks)
        #print("Open Market",ZerodhaConnect.open_time)            
        #print("Closed Market",ZerodhaConnect.close_time)            
        #self.stratergy.actions(ticks)
        now = dt.datetime.now() 
        if now > ZerodhaConnect.open_time and now < ZerodhaConnect.close_time:
            print("Market Open")
            stocks = self.get_subscribed_ticker()
            text = self.user_name + ":-" + str(stocks)
            #self.mailer.mail(subject='Trading Bot Started For These Stocks', text=text)
            self.on_ticks = self._tick_consumer
    
