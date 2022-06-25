from fyers.script import name_to_script
from datetime import *
from datetime import datetime
import re
#cache={}
class history:
    '''name,fyers,days=5,resolution="1m",date_format="0",range_from=None,range_to=None,cont_flag="1"'''
    def __init__(self,fyers):
        self.fyers=fyers.fyers
        self.cache={}
        #self.days=days
        #self.resolution=resolution
        #self.date_format=date_format
        #self.range_from=range_from
        #self.range_to=range_to
        #self.cont_flag=cont_flag
    def history(self,name,days=50,resolution="1",date_format="1",range_from=None,range_to=None,cont_flag="1"):
        name=name_to_script(name)
        if range_from == None:
            range_from = (datetime.now() - timedelta((days))).strftime('%Y-%m-%d')
        if range_to == None:
            range_to=str((datetime.now() + timedelta((1))).strftime('%Y-%m-%d'))
            #range_to = str(date.today())
        try:
            #print('Returning value in cache ')
            #print(self.cache)
            ttt=re.sub(':|-', '', str(str(name)+str(resolution)+str(date_format)+str(range_from)+str(range_to)+str(cont_flag)))
            return self.cache[ttt]
        except:
            print('not able to return value in cache ')
            try:
                data = {"symbol":name,"resolution":resolution,"date_format":date_format,"range_from":range_from,"range_to":range_to,"cont_flag":cont_flag}
                uuu=self.fyers.history(data)
                self.cache.update({re.sub(':|-', '', str(str(name)+str(resolution)+str(date_format)+str(range_from)+str(range_to)+str(cont_flag))):uuu})
                #print(self.cache.keys())
                return uuu
            except Exception as error:
                print(f'There is an error while fetching Historical data from fyers   : {error}')

