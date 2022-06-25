import os 
import pandas as pd
n=0
y=0
m=-4
for k in range(68,1,-1):
    n=10000
    m=m+1
    for i in os.listdir('data'):
        try:
            d=pd.read_csv('data/'+i)
            d['pc']=((d['close']-d['open'])/d['open'])*100
            #d=d.sort_values(by='pc',ascending=False)
            c=d['pc'].iloc[k]
            d['name']=i[:-4]
            #d['name'][0]
            if n>c:
                n=c
                d.to_csv(f'toploosers/{m}.csv')
                print(y)
                print(d['name'][0])
                y+=1
        except Exception as error:
            print(error)        
