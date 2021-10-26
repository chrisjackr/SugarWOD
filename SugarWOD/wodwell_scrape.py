# ====== AUXILARY SCRIPT TO CREATE MOVEMENTS LIST ====== #
# This auxilary script was used to help generate movements.txt file.
# This is a list of different crossfit exercises, e.g. running, snatch, pull-up etc.
# The movements.txt file is edited to also include name variations so this will NOT recreate file exactly.

# ====== IMPROVEMENTS ====== #
# 

import requests
from bs4 import BeautifulSoup
import re
import csv

def scrape_data(url):
    with requests.Session() as s:
        p = s.get("https://wodwell.com/",headers=headers)
        login_text = p.text
        soup = BeautifulSoup(login_text,'html.parser')
        print(soup.prettify())

def create_csv():
    # Used to help create movements.txt file (otherwise to be copied from WODwell website)
    with open(r'C:\Users\cjr19\Python\Repositories\SugarWOD\BrowseWorkoutCollections_Movement.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f,'html.parser')
        all = soup.find_all('a', class_="wod-collections-list__item")
        all = [item.text for item in all]
        #pprint.pprint(all)

        scores = [['AMRAP'],['EMOM'],['For Load'],['For Time'],['Tabata'],['Partner']]
        #print(score)

        movements = all[14:124]
        movements = [move.strip('\n ') for move in movements]
        comp = re.compile('[\'\/a-zA-Z\s-]+') 
        movements = [re.match(comp,move)[0].rstrip() for move in movements]
        movements.sort()
        movements = [[move] for move in movements]
        #print(movements)

        with open('movements_csv','w',newline='') as f:
            write = csv.writer(f)
            write.writerows(movements)
        
        with open('scores_csv','w',newline='') as f:
            write = csv.writer(f)
            write.writerows(scores)

if __name__ == '__main__':
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    scrape_data("https://wodwell.com/")
    create_csv()

