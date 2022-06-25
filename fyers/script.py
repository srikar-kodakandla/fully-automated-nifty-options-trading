from common import message as m
def name_to_script(name):
    try:
        import os
        import pandas as pd
        import re
        try:
            a = pd.read_csv('NSE_CM.csv.1')
        except:
            os.system('wget https://public.fyers.in/sym_details/NSE_CM.csv')
        finally:
            try:
                a = pd.read_csv('NSE_CM.csv.1')
            except:
                os.system('wget https://public.fyers.in/sym_details/NSE_CM.csv')
                a = pd.read_csv('NSE_CM.csv.1')
        try:
            dd=sorted(a[a['NSE:AMARAJABAT-EQ'].str.contains(name, flags=re.IGNORECASE)]['NSE:AMARAJABAT-EQ'].to_numpy())[0]
        except:
            try:
                dd=sorted(a[a['AMARA RAJA BATTERIES LTD.'].str.contains(name, flags=re.IGNORECASE)]['NSE:AMARAJABAT-EQ'].to_numpy())[0]
            except:
                vv = a[a['INE885A01032'].notna()]
                dd = vv[vv['INE885A01032'].str.contains(name, flags=re.IGNORECASE)]['NSE:AMARAJABAT-EQ'].to_numpy()[0]
    except Exception as error :
        m.message(f'Either the stock name is wrong or error while downloading data from fyers website \n{error}')
    try:
        return dd
    except Exception as error:
        m.message(f"can't find the given stock name {error}")
    return False