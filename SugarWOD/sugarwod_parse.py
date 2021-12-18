# ====== READ_HTML_FILES_&_PARSES INFO ====== #
# Creates a dictionary from each week file with the following format:
# week = {date1: workouts1, date2: workouts2, ..., date7: workouts7}
#                --> workouts = {title1: desc1 ,t2:d2 ,t3:d3, ... }

# ====== IMPROVEMENTS ====== #
# 

from bs4 import BeautifulSoup
import pprint
import datetime
import os
import json
from sugarwod_scrape_v1 import create_list_to_save
import credentials as creds


# =========== AUXINLARY DEFINITIONS =========== #

def parse_week_file(weekdate, show=False):
    weekdate = str(weekdate)

    # === CREATE MONTHS YEAR LIST === #
    monthyear = datetime.datetime(int(weekdate[:4]),int(weekdate[4:6].lstrip('0')),int(weekdate[6:].lstrip('0')))
    months = [monthyear.strftime(r'%Y')+monthyear.strftime(r'%m')]
    tdelta = datetime.timedelta(days=1)
    for i in range(6):
        monthyear = monthyear + tdelta
        months.append(monthyear.strftime(r'%Y')+monthyear.strftime(r'%m'))
    #print(months)
    

    with open(os.getcwd()+f'\\HTML_files_{creds.gym}\\wod_{weekdate}.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f,'html.parser')

        # === CREATES DATES LIST === #
        dates = soup.find_all("h3", class_="cal-day-header-title")[:-1]
        dates = [date.text[-2:] for date in dates]
        #print(dates)

        workouts_list = []
        days = soup.find_all("div","cal-day-body")
        for day in days:
            # === CREATES WORKOUT TITLES LIST === #
            titles = day.find_all("span", class_="cal-workout-title")
            titles = [title.text for title in titles]
            titles = [str(title.replace("\'","\'\'").strip("\'\" ")) for title in titles]
            titles = [str(title.replace('\"','').strip("\'\" ")) for title in titles]

            #print(titles)

            # === CREATES WORKOUT DESCRIPTIONS LIST === #
            descriptions = day.find_all("p", class_="cal-workout-description")
            #descriptions = [description.text for description in descriptions]
            new_descriptions = []
            for description in descriptions:
                for br in description.find_all("br"):
                    br.replace_with("\n")
                new_descriptions.append(description.text)
            #print(new_descriptions)
            new_descriptions = [str(d.replace("\'","\'\'").strip("\'\" ")) for d in new_descriptions]
            workouts = dict(zip(titles,new_descriptions))
            #pprint.pprint(workouts)
            workouts_list.append(workouts)
        
        # === CONCATENATES DATES & MONTHS LISTS === #
        datemonth = [m+d for d,m in zip(dates,months)]

        # === CREATES WEEK DICTIONARY === #
        week = dict(zip(datemonth,workouts_list))
        if show: 
            pprint.pprint(week)
        
        print('WeekDate '+weekdate+' successfully parsed...')
        return(week)

def display_json():
    with open(os.getcwd()+f"\\sugarwod_{creds.gym}_json.json","r") as f:
            all_weeks = json.load(f)
    pprint.pprint(all_weeks)



# =========== MAIN PARSE DEFINITION =========== #

def sugarwod_parse(scrape_dates=[], reset = False):
    print('\n========= START PARSING HTML PAGES =========\n')
    weekdate_list = scrape_dates
    #print(weekdate_list)
        
    # ================ RESETS JSON FROM SCRATCH BY PARSING ALL HTML FILES ==============================
    if reset:
        weekdate_list = os.listdir(os.getcwd()+f"\\HTML_files_{creds.gym}")
        weekdate_list = [date[4:12] for date in weekdate_list]
        weekdate_list = list(set(weekdate_list))
        weekdate_list.sort()
        with open(os.getcwd()+f"\\sugarwod_{creds.gym}_json.json","w") as f:
            f.truncate(0)
            f = json.dump({},f)
    # ====================================================================================================

    if weekdate_list:
        fails, count = 0, 0
        print('Number of weeks: ',len(weekdate_list),'\n')
        for weekdate in weekdate_list:
            count += 1
            try:
                week = parse_week_file(weekdate)
                with open(os.getcwd()+f"\\sugarwod_{creds.gym}_json.json","r") as f:
                    all_weeks = json.load(f)
                all_weeks = dict(all_weeks, **week)
                with open(os.getcwd()+f"\\sugarwod_{creds.gym}_json.json","w") as f:
                    f = json.dump(all_weeks,f)
            
            except:
                print('WeekDate '+weekdate+' FAILED parse.')
                fails += 1

        perc = ((count-fails)/count)*100
        print('\nParsing '+str(round(perc,2))+'% Successful\nJson updated.')
    else:
        print('No new weekdates to add to .json file.\n')
    
    #display_json()


if __name__ == '__main__':
    sugarwod_parse(reset=False)