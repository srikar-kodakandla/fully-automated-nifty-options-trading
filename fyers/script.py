from common import message as m
def name_to_script(name):
    try:
        import os
        import pandas as pd
        import re
        try:
            a = pd.read_csv('NSE_CM.csv')
            #print("current working directory......",os.getcwd())
           # print(a)
        except:
            os.system('curl -0 https://public.fyers.in/sym_details/NSE_CM.csv')
            #print("exception 1......................")
        finally:
            try:
                a = pd.read_csv('NSE_CM.csv')
                #print("finally1....")
            except:
                os.system('curl -0 https://public.fyers.in/sym_details/NSE_CM.csv')
                a = pd.read_csv('NSE_CM.csv')
                
        try:
            #print("before dd values......")
            dd=sorted(a[a['NSE:ABAN-EQ'].str.contains(name, flags=re.IGNORECASE)]['NSE:AMARAJABAT-EQ'].to_numpy())[0]
           
        except:
            try:
                #print("dd2 values..")
                dd=sorted(a[a['ABAN OFFSHORE LTD.'].str.contains(name, flags=re.IGNORECASE)]['NSE:ABAN-EQ'].to_numpy())[0]
                
            except:
                #print("dd3 values....vv values")
                vv = a[a['INE421A01028'].notna()]
                dd = vv[vv['INE421A01028'].str.contains(name, flags=re.IGNORECASE)]['NSE:ABAN-EQ'].to_numpy()[0]
                
    except Exception as error :
        m.message(f'Either the stock name is wrong or error while downloading data from fyers website \n{error}')
    try:
        return dd
    except Exception as error:
        m.message(f"can't find the given stock name {error}")
    return False
