# ====== LOGIN_TO_SUGARWOD_&_SAVE_PAGES ====== #
# The following code logs into SugarWOD, loads and saves calendar webpages as
# html files so that they can later be opened and parsed. The script creates a 
# list of all weeks which have not already been saved to the HTML_files folder,
# then sequential loads and saves these pages.

# ====== IMPROVEMENTS ====== #
# Check download or webpage loaded instead of time.sleep()


import re
import credentials as creds

import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

import time
import datetime
import os

# =========== AUXILARY DEFINITIONS =========== #

def login(browser,email, password):
    # Fills out and submits login page form.
    try:
        email = browser.find_element_by_id("inputEmail")
        password = browser.find_element_by_id("inputPassword")
    except:
        print('\nCould not enter login details.\n')
        quit()

    email.send_keys('cjr1977@hotmail.co.uk')
    password.send_keys('SugarWOD123!')          
    password.send_keys(Keys.ENTER)

def save_page(save_name):
    # Saves the current webpage as an html file in HTML_files folder.
    pyautogui.hotkey('ctrl','s')
    time.sleep(10)
    file_name = 'C:\\Users\\cjr19\\Python\\Repositories\\SugarWOD\\HTML_files\\wod_'+save_name+'.html'
    pyautogui.typewrite(file_name.lower())
    pyautogui.hotkey('enter')
    print(f'Week {save_name} saved...')

def create_list_to_save():
    # Creates a list of all weeks to save which have not already been saved.
    start = datetime.datetime(2020,7,27) # starting week (could change for different gym)
    now = datetime.datetime.today()
    tdelta = datetime.timedelta(days=7)
    next_date = start
    all_dates = [start.date().strftime(r'%Y%m%d')]
    while next_date < (now - tdelta):
        next_date = next_date + tdelta
        all_dates.append(next_date.date().strftime(r'%Y%m%d'))
    
    done_dates = os.listdir("C:\\Users\\cjr19\\Python\\Repositories\\SugarWOD\\HTML_files")
    done_dates = [date[4:12] for date in done_dates]
    scrape_dates = list(set(all_dates)-set(done_dates))
    if bool(scrape_dates):
        # If new weeks to be scrape, sort chronologically.
        scrape_dates = [int(date) for date in scrape_dates]
        scrape_dates.sort()
        scrape_dates = [str(date) for date in scrape_dates]
        scrape_dates = scrape_dates[:-1]                               #do not use most recent week (because not all days complete)
        print('\nNew weeks to scrape: \n',scrape_dates,'\n')
        return scrape_dates
    else:
        # If no new weeks, end.
        print('\nNo new week pages to save.\n')
        quit()



# =========== MAIN SCRIPT DEFINITION =========== #

def sugarwod_scrape_v1():
    print('\n========= START SCRAPING HTML PAGES =========\n')
    # Open selenium webbrowser.
    try:
        # PATH = "C:\Program Files (x86)\chromedriver.exe"
        # PATH = r"C:\Users\Owner\.wdm\drivers\chromedriver\win32\87.0.4280.20\chromedriver.exe"      
        PATH = os.path.normpath(r"C:\Users\cjr19\.wdm\drivers\chromedriver\win32\95.0.4638.17\chromedriver.exe")          #This is where chromedriver is saved for your computer
        browser = webdriver.Chrome(PATH)
    except:
        browser = webdriver.Chrome(ChromeDriverManager().install())                                                       #If webdriver cannot locate up-to-date chromedriver.exe, then it will automatically download necessary file and use that.
        print('\nNEW DRIVER CHANGE PATH')

    browser.get('https://app.sugarwod.com/workouts/calendar?week=20200727&track=workout-of-the-day')
    time.sleep(5)
    login(browser,creds.email, creds.password)
    time.sleep(5)
    scrape_dates = create_list_to_save()

    for date in scrape_dates:
        # Load each week's webpage and save as html file.
        browser.get('https://app.sugarwod.com/workouts/calendar?week='+date+'&track=workout-of-the-day')
        time.sleep(15)
        save_page(date)
        time.sleep(15)
    
    print('Page scraping complete.')
    return scrape_dates




if __name__ == '__main__':
    sugarwod_scrape_v1()   