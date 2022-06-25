#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 23:49:28 2020

@author: harpal
"""

import os
import threading
import datetime
import queue
import time
import pandas as pd
class TickLogger():
    def __init__(self, csv_file_name, tick):
        #No Need to save following
        del tick['symbol']
        del tick['exchange']
        if 'bid_table' in tick:
            tick['bid_table'] = str(tick['bid_table'].to_dict())
        if 'offer_table' in tick:
            tick['offer_table'] = str(tick['offer_table'].to_dict())
        self.csv_file_name = csv_file_name
        self.pd = pd.DataFrame()
        self.pd = self.pd.append(tick, ignore_index=True)
        #If Log file not created then only create log file
        if not os.path.exists(csv_file_name):
            self.pd.to_csv(self.csv_file_name, index = False) 
            self.pd = self.pd[0:0]
        
    def append(self,tick):
        del tick['symbol']
        del tick['exchange']
        if 'bid_table' in tick:
            tick['bid_table'] = str(tick['bid_table'].to_dict())
        if 'offer_table' in tick:
            tick['offer_table'] = str(tick['offer_table'].to_dict())
        self.pd = self.pd.append(tick, ignore_index=True)
        
    def save(self):
        self.pd.to_csv(self.csv_file_name, mode='a', header=False, index = False) 
        self.pd = self.pd[0:0]
        

class StockLogger(threading.Thread):
    def __init__(self, base_path='/home/harpal/Desktop/StockHistorical/data', chunk_size = 10):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.date = date = datetime.datetime.now().date()
        self.base_path = base_path
        self.ticks_queue = queue.Queue(500)
        if base_path:
            self.base_path = base_path
            
        self.__logger_dict = {'NSE':{},'BSE':{}}      
        self.stop_flag = False
        self.chunk_size = chunk_size
        self.count = 0
        self.last_ticks={}
        #self.cur_time = None
        
    
    def __log_into_panda(self,ticks):
        self.count += 1
        #print(self.count)
        for tick in ticks:
            #if self.cur_time == tick['timestamp']:
                #continue
            #self.cur_time = ticks['timestamp']
            symbol = tick['symbol']
            exchange = tick['exchange']
            
            # Don't save too much data 
            #last_tick = self.last_ticks.get(exchange+symbol)
            #if last_tick:
                # Don't save more then one tick per secound
                #if last_tick['timestamp'] == tick['timestamp'] :
                    #continue
                # Don't save repeating price tick
                #if last_tick['ltp'] == tick['ltp'] :
                    #continue
            #self.last_ticks[exchange+symbol] = tick
            if self.__logger_dict[exchange].get(symbol,None):
                self.__logger_dict[exchange][symbol].append(tick)
            else:
                log_path = self.base_path+'/'+exchange+'/'+symbol               
                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                    
                log_file = log_path +'/'+str(self.date)+'.csv' 
                self.__logger_dict[exchange][symbol] = TickLogger(csv_file_name = log_file, tick=tick)
    
    def save_to_files(self):
        for exchange in self.__logger_dict:
            exchange_temp = self.__logger_dict[exchange]
            for tick_logger in exchange_temp:
                exchange_temp[tick_logger].save()
                
    def stop(self):
        self.stop_flag = True
        
    def log_ticks(self,ticks):
        if not self.ticks_queue.full():
            self.ticks_queue.put(ticks)
        else:
            print('Hs Logger Queue is Full')
        
                
    def run(self):
        while True:
            while not self.ticks_queue.empty():
                ticks = self.ticks_queue.get()
                self.__log_into_panda(ticks)
            
            if self.count >= self.chunk_size:
                self.count = 0
                self.save_to_files()
                 
            if self.stop_flag:
                self.save_to_files()
                break
            time.sleep(10)
                
                 
        
                
            
            
