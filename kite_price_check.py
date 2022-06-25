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
from common.message import message
def login():
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('—disable-gpu')
    #options.headless=True
    from selenium import webdriver
    from webdriver_manager.firefox import GeckoDriverManager
    driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
    driver.get('https://kite.zerodha.com/dashboard')
    driver.find_element_by_xpath('//*[@id="userid"]').send_keys('KI3644')
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('Nanna143!')
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/form/div[4]/button').click()
    driver.find_element_by_xpath('//*[@id="pin"]').send_keys('825556')
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div/div/form/div[3]/button').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/a[4]/span').click()
    return driver
driver=login()
#sleep(20)
while True:
    sleep(10)
    try:
        #sleep(5)
        price=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/section[2]/div/div/table/tfoot/tr/td[3]').text
        if price<5000:
            message(price)
        print(price)
    except:
        print('There is an error in the website , logining in again ...')
        message('There is an error in website of kite.... please check')
        #driver=login()
