import urllib.parse as urlparse
from time import sleep
import pdb
from fyers_api import fyersModel, accessToken
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from common import message as m
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
"""try :
    cre = open('cred.txt').read().split('\n')
except:
    cre=open('fyers/cred.txt').read().split('\n')
user_id = cre[0]
password= cre[1]
two_fa= cre[2]
redirect_url='http://127.0.0.1/'
app_id = cre[3]
app_secret= cre[4]"""


class login:
    def __init__(self, cred):
        self.user_id = cred[0]
        self.password = cred[1]
        self.two_fa = cred[2]
        self.redirect_url = cred[5]
        # redirect_url = 'http://127.0.0.1/'
        self.app_id = cred[3]
        self.app_secret = cred[4]

    def get_token(self):
        session = accessToken.SessionModel(client_id=self.app_id,
                                           secret_key=self.app_secret,
                                           redirect_uri=self.redirect_url,
                                           response_type="code",
                                           grant_type="authorization_code")
        url = session.generate_authcode()
        options = Options()
        """options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)"""
        from selenium import webdriver
        from webdriver_manager.firefox import GeckoDriverManager
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())

        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="fy_client_id"]')))
        
        driver.find_element_by_xpath('//*[@id="fy_client_id"]').send_keys(self.user_id)
        driver.find_element_by_xpath('//*[@id="clientIdSubmit"]').click()
        driver.find_element_by_xpath('//*[@id="fy_client_pwd"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="loginSubmit"]').click()
        driver.find_element_by_css_selector('input.pin-field:nth-child(1)').send_keys(8)
        driver.find_element_by_css_selector('input.pin-field:nth-child(2)').send_keys(2)
        driver.find_element_by_css_selector('input.pin-field:nth-child(3)').send_keys(5)
        driver.find_element_by_css_selector('input.pin-field:nth-child(4)').send_keys(6)
        try:
            driver.find_element_by_xpath('//*[@id="verifyPinSubmit"]').click()
        except Exception as error:
            print('Ignorable error ',error)    
        #driver.find_element_by_xpath("//input[@id='pancard']").send_keys(self.two_fa)
        #driver.find_element_by_xpath("//button[@id='btn_id']").click()
        sleep(10)
        current_url = driver.current_url
        sleep(5)
        driver.close()
        parsed = urlparse.urlparse(current_url)
        #pdb.set_trace()
        auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
        session.set_token(auth_code)
        response = session.generate_token()
        return response['access_token']

    def login(self,user_id='unknown_user_id'):
        auth_code = self.get_token()
        access_token = auth_code
        #pdb.set_trace()
        fyers = fyersModel.FyersModel(client_id=self.app_id, token=access_token, log_path="../fyers")
        m.message(f'Login done for {self.app_id}')
        import pickle
        self.fyers = fyers
        self.auth_code = auth_code
        self.token = auth_code
        with open(f'{user_id}', 'wb') as disk:
            pickle.dump(self, disk)
        # return fyers,auth_code


if __name__ == '__main__':
    access_token = self.get_token()
    print(access_token)
    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token, log_path="../fyers")
    print(fyers.get_profile()["code"])

    orderbook = fyers.orderbook()
    print(orderbook)
    if orderbook["code"] == 200:
        print(orderbook["orderBook"])
    else:
        print('Error Fetching Orderbook')
