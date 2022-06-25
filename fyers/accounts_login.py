from fyers.login import login
import pandas as pd
try:
    h=pd.read_csv(('fyers/cred.csv'))
except :
    h = pd.read_csv(('cred.csv'))
accounts=[]
def login_accounts(h=h):
    u=[]
    for i in h:
        accounts.append(login(h[i]))
        u.append(i)
    for i in range(len(accounts)):
        try:
            accounts[i].login(u[i])
        except Exception as error:
            print(f'There is an error in login {error}')
    return accounts


