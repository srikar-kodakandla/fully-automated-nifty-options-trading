import pandas as pd
data=pd.read_csv('Fyers - Scrips blocked for Intraday trading - Equity.csv')
data=data['List of Scrips blocked for Intraday trading']
data=data.tolist()
def allow(a,data=data):
    allowed=[]
    not_allowed=[]
    for i in a:
        if i not in data:
            allowed.append(i)
        else:
            not_allowed.append(i)
            
    return allowed


