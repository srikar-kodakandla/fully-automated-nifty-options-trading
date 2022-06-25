import time
import os
import pandas as pd
import sqlite3
from datetime import datetime
import sys
if os.getcwd()[0] == 'C':
    db = sqlite3.connect('ticks.db')
else:
    db = sqlite3.connect('ticks.db',check_same_thread=False)
def create_tables(tokens):
    c = db.cursor()
    print(" i am in creating table ")
    for i in tokens:
        print("CREATE TABLE IF NOT EXISTS TOKEN{} (ts datetime primary key,price real(15,5), volume integer)".format(i))
        c.execute("CREATE TABLE IF NOT EXISTS TOKEN{} (ts datetime primary key,price real(15,5), volume integer)".format(i))
    try:
        db.commit()
    except:
        db.rollback()

def insert_ticks(ticks):
    
    c = db.cursor()
    #print(' I am in insert_ticks')
    #print('i am in insert ticks bro ')
    for tick in ticks:
        try:
            #print()
            #print(tick)
            #print()
            tok = str(tick['symbol'])
            #print(tok)
            tok= tok.split('-')[0].split(':')[1]
            #print(tok)
            vals = [datetime.now(), tick['ltp'], tick['min_volume']]
            #print(vals)
            query = "INSERT INTO TOKEN{}(ts,price,volume) VALUES (?,?,?)".format(tok)
            #print(query)
            c.execute(query, vals)
        except Exception as error:
            try:
                tok = str(tick['symbol'])
                tok = tok.split('-')[0].split(':')[1]
                create_tables([tok])
                print(error)
            except Exception as error:
                print(error)
                print('same value entered twice to the database table ')

    try:
        db.commit()
    except Exception as error:
        print(error)
        db.rollback()
        print('Same timestamp tried to added !!!')

