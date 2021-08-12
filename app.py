
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
#import datetime
import time
import re


class KakaoPost:
    
    def __init__(self):
        self.friend_count = 0
        self.my_url = 'https://pf.kakao.com/_ZwCrT'
        self.page_soup = ''
        
    def scroll(self, driver, timeout):
        #Function to scroll the webpage till the end
        scroll_pause_time = timeout
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def run_driver(self):
        #Function to configure and run the driver. 
        options = Options()
        options.add_argument("--headless")
        #options.add_argument("--remote-debugging-port=9222")
        #options.add_argument("window-size=1400,1500")
        #options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        #options.add_argument("start-maximized")
        #options.add_argument("enable-automation")
        #options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path = '/var/task/chromedriver', options=options)
        driver.implicitly_wait(15)
        driver.get(self.my_url)
        driver.find_elements_by_class_name('link_menu')[1].click()
        self.scroll(driver, 5)
        self.page_soup = soup(driver.page_source, features ="html.parser")
        driver.close()        

    def get_friends(self):
        #Function to get the friend count from the page html
        friend_count = self.page_soup.find("span",{"class":"txt_friends"}).text
        friend_count = ''.join(re.findall("\d+", friend_count))
        return friend_count
    

def lambda_handler(event, context):
    k1 = KakaoPost()
    k1.run_driver()
    count = k1.get_friends()
    return {
        "statusCode": 200,
        "body": count
    }

