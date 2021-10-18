#LoginSugarWOD

import requests_html
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathlib import Path
import sqlite3

import time
import datetime
import os



# def scrape_data(url):
#     headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
#     # page = re.get(url,headers=headers)
#     # print(page.text)
#     # session = requests_html.HTMLSession()
#     # r = session.get(url,headers=headers)
#     # r.html.render(sleep=2, timeout=5)
#     # print(r.text)
#     # for  item in r.html.xpath(xpath):
#     #     items_string = item.text
    
#     payload = {'inUserName': 'cjr1977@hotmail.co.uk',
#                'inUserPass': 'SugarWOD123!'}

#     # Use 'with' to ensure the session context is closed after use.
#     with requests.Session() as s:
#         p = s.post(url, data=payload, headers=headers)
#         # print the html returned or something more intelligent to see if it's a successful login page.
#         print(p.text)

#         # An authorised request.
#         r = s.get('A protected web page url')
#         print(r.tex)


url = "https://app.sugarwod.com/workouts/calendar?week=20200803&track=workout-of-the-day"
email = 'cjr1977@hotmail.co.uk'
password = 'SugarWOD123!'

if __name__ == '__main__':
    try:
        # PATH = "C:\Program Files (x86)\chromedriver.exe"
        # PATH = r"C:\Users\Owner\.wdm\drivers\chromedriver\win32\87.0.4280.20\chromedriver.exe"      
        PATH = os.path.normpath(r"C:/Users/cjr19/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver.exe")          #This is where chromedriver is saved for your computer
        driver = webdriver.Chrome(PATH)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install())                                      #If webdriver cannot locate up-to-date chromedriver.exe, then it will automatically download necessary file and use that.
        print('NEW DRIVER CHANGE PATH')

driver.get('https://app.sugarwod.com/login')
#time.sleep(2.5)

#---------------LOGIN------------------#
try:
    email = driver.find_element_by_id("inputEmail")
    password = driver.find_element_by_id("inputPassword")
except:
    print('Could not enter login details.')
    quit()

email.send_keys("cjr1977@hotmail.co.uk")                             #!!!_ADD_EMAIL_ADDRESS_!!!#
password.send_keys("SugarWOD123!")                                        #!!!_ADD_PIN_NUMBER_!!!#
password.send_keys(Keys.ENTER)
#---------------------------------------#
time.sleep(10)
print('Done')