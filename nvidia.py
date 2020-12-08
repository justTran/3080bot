import json, os, requests, time
from datetime import datetime
from pprint import pprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge
from msedge.selenium_tools import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Nvidia():

    def __init__(self):
        self.api = 'https://api-prod.nvidia.com/direct-sales-shop/DR/products/en_us/USD/5438481700' #nvidia-api
        self.debug = 'https://jsonplaceholder.typicode.com/todos/2'
        self.options = EdgeOptions()
        self.options.use_chromium = True
        self.options.add_argument("--user-data-dir=C:\\Users\\Justin\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1") #Path to your chrome profile
        self.script = '''javascript:store.dispatch({type: actionTypes.ADD_ITEM_TO_CART,id: 5438481700,quantity: 1});
                        document.getElementsByClassName('nv-button js-checkout cart__checkout-button')[0].click();'''
        self.driver = Edge(executable_path = os.getcwd() +  '/msedgedriver.exe')
        print(f'\033[91m{datetime.now().strftime("%H:%M:%S")}\033[00m \033[94m[Browser]\033[00m Browser is open!')
        self.wait = WebDriverWait(self.driver, 10)
        self.test()

    def test(self):
        print(f'\033[91m{datetime.now().strftime("%H:%M:%S")}\033[00m \033[94m[Browser]\033[00m Going to NVIDIA')
        self.driver.get("https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3080/")
        self.makeRequest()

    def purchaseScript(self):
        try:
            self.driver.execute_script(self.script)
            time.sleep(2)
            self.driver.get('https://store.nvidia.com/store?Action=DisplayPage&Locale=en_US&SiteID=nvidia&id=QuickBuyCartPage')
            print(f'{datetime.now().strftime("%H:%M:%S")} \033[92m[Status]\033[00m Bought')
        except:
            print(f'{datetime.now().strftime("%H:%M:%S")} \033[92m[Status]\033[00m JavaScript Error')
    
    def makeRequest(self):
        while(1):
            r = requests.get(self.api) #CHANGE TO API
            if r.status_code != 200:
                print(f'\033[91m{datetime.now().strftime("%H:%M:%S")}\033[00m \033[92m[Status]\033[00m \033[96mAPI Cooldown.... waiting 30 seconds\033[00m')
                time.sleep(30)
            else:

                if r.json()["InventoryStatus"]["status"] == 'PRODUCT_INVENTORY_OUT_OF_STOCK':
                    print(f'\033[91m{datetime.now().strftime("%H:%M:%S")}\033[00m \033[92m[Status]\033[00m \033[91mOUT OF STOCK\033[00m')
                    time.sleep(1.5)

                else:
                    self.purchaseScript()
                    break

if __name__ == "__main__":
    Nvidia()


