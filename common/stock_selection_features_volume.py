import urllib.parse as urlparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.utils import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from common import message as m
options = Options()
#options.add_argument('--headless')
#options.add_argument('—disable-gpu')
options.headless=True
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
from selenium.webdriver.common.keys import Keys
#driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM
#).install(), options=options)
#driver.get('https://chartink.com/screener/copy-high-volatile-stocks-day-trade-or-btst-338')
#driver.get('https://chartink.com/screener/copy-high-volume-stocks-3207')
#driver.get('https://chartink.com/screener/copy-high-volume-stocks1-1')#driver.get('https://chartink.com/screener/relative-high-volume-stocks')
driver.get('https://chartink.com/screener/relative-high-volume-stocks-with-volume-shockers')
stock=[]
for k in range(20,0,-1):
    print(k)
    driver.get('https://chartink.com/screener/relative-high-volume-stocks-with-volume-shockers')
    WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/ul/li[4]/span/span[4]/span[5]/span[2]/span/span/span'))).click()
    for i in range(10):
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/ul/li[4]/span/span[4]/span[5]/span[2]/span/span/input'))).send_keys(Keys.BACKSPACE)
    WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/ul/li[4]/span/span[4]/span[5]/span[2]/span/span/input'))).send_keys(k)
    WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]'))).click()
    count=0
    while count<25 :
        count+=1
        try:
            stock.append(WebDriverWait(driver,0.1).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{count}]/td[3]/a'))).text)
            print(stock[-1])
        except:
            pass
            #print("There is no stock in the given XPATH...")

res = []
for i in stock:
    if i not in res:
        res.append(i)
stock=res
#stock=driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[3]/a').text
write=open('stock_selection.txt','w')
for i in stock:
    write.write(i)
    write.write('\n')
write.close()
m.message(f'Selected the following stock to trade tomorrow is {stock}')
driver.close()
