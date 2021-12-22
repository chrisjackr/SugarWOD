# ====== CREATE_SQL_DATABASE ====== #
#

# ====== IMPROVEMENTS ====== #
# 

import sqlite3
from sqlite3 import Error
import credentials as creds
import os
import json
from progress.bar import Bar
from sugarwod_scrape_v1 import create_list_to_save
import datetime

# def create_csv():
#     # Used to help create movements.txt file (otherwise to be copied from WODwell website)
#     with open(r'C:\Users\cjr19\Python\Repositories\SugarWOD\BrowseWorkoutCollections_Movement.html', encoding='utf-8') as f:
#         soup = BeautifulSoup(f,'html.parser')
#         all = soup.find_all('a', class_="wod-collections-list__item")
#         all = [item.text for item in all]
#         #pprint.pprint(all)

#         scores = [['AMRAP'],['EMOM'],['For Load'],['For Time'],['Tabata'],['Partner']]
#         #print(score)

#         movements = all[14:124]
#         movements = [move.strip('\n ') for move in movements]
#         comp = re.compile('[\'\/a-zA-Z\s-]+') 
#         movements = [re.match(comp,move)[0].rstrip() for move in movements]
#         movements.sort()
#         movements = [[move] for move in movements]
#         #print(movements)

#         with open('movements_csv','w',newline='') as f:
#             write = csv.writer(f)
#             write.writerows(movements)
        
#         with open('scores_csv','w',newline='') as f:
#             write = csv.writer(f)
#             write.writerows(scores)


def create_table(file_name,headers):
    #creates table if it does not exist
    conn = None
    try:
        conn = sqlite3.connect(file_name)
        conn.execute(headers)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def insert_workout_table(file_name,headers,insert):
    conn = None
    try:
        conn = sqlite3.connect(file_name)
        conn.execute(f'''INSERT INTO sugarwod_{creds.gym}_table {headers} VALUES {insert};''')
    
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_values_list(file,values):
    # Creates list with all movements/types from movements.txt
    with open(file,'r') as f:
        for line in f:
            if line.startswith('#'):
                pass
            else:
                values.append(line.strip('\n'))

def search(text_to_search,values,show=False):
    if show:
        print('\n',text_to_search,'\n')
    values_list=[0]*len(values)
    for i,val in enumerate(values):
        subvalues = val.split('/')
        exists = 'N'
        for subval in subvalues:
            if subval.lower() in text_to_search:
                exists = 'Y'
                values_list[i] = 1
                break
        if show:
            print(val.lower(),': ', exists)  
    return values_list
 
def create_values_string(values_list,all_weeks,weekdate,key):
    values_list = [str(val) for val in values_list]
    values_list = ','.join(values_list)
    weekday = str(datetime.datetime(int(weekdate[0:4]),int(weekdate[4:6]),int(weekdate[6:8])).strftime('%A'))
    values_string = f"({weekdate},'{weekday}','{key}','{all_weeks[weekdate][key]}',{values_list},NULL)"
    return values_string


def check_name(file_name,column,weekdate):
    conn = None
    try:
        conn = sqlite3.connect(file_name)
        conn.execute(f'''UPDATE sugarwod_{creds.gym}_table
                        SET {column} = 1
                        WHERE WeekDate = {weekdate}''')
    
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def sugarwod_table(scrape_dates=[],reset = False):
    print('\n========= START CREATING SQL DATABASE =========\n')
    #create_csv()
    headers = ''
    columns = ''
    #Create headers from movements.text to use when creating table...
    with open(os.getcwd()+f"\\movements.txt",'r') as f:
        for line in f:
            if line.startswith('#'):
                pass
            else:
                headers = headers + '[{}] BOOL, '.format(line.strip('\n').split('/')[0])
                columns = columns +'"{}",'.format(line.strip('\n').split('/')[0])
    all_headers = f'''CREATE TABLE IF NOT EXISTS  sugarwod_{creds.gym}_table ([WeekDate] TEXT, [Weekday] TEXT, [Title] TEXT, [Workout] TEXT, {headers}[STAR] BOOL)'''
    all_columns = f'''(WeekDate,Weekday,Title,Workout,{columns}STAR)'''

    #Create list of all weekdates (that should be saved in json file) to be itereated through when adding info to table,
    with open(os.getcwd()+f"\\sugarwod_{creds.gym}_json.json","r") as f:
        all_weeks = json.load(f)
    
    if reset:
        # If reset, delete database file and create list of all available dates.
        try:
            os.remove(os.getcwd()+f"\\sugarwod_sql.db")
        except FileNotFoundError:
            print('No database exists, creating new file...')
        weekdates = list(all_weeks.keys())
        #pprint.pprint(all_weeks)
    else:
        # Otherwise use only weekdates just scraped.
        weekdates = scrape_dates

    create_table(os.getcwd()+f"\\sugarwod_sql.db",all_headers)
    #print(all_headers)

    #=============TEST_DATE=============#
    #test_date = {'20210602':all_weeks['20210602']}
    #print(test_date)
    #all_weeks = test_date
    #===================================#

    #========================CHECK_EXERCISES======================#
    movements = []
    create_values_list(os.getcwd()+'\\movements.txt',movements)

    #print(list(all_weeks.keys()))
    with Bar('Generating Database...', max=len(weekdates)) as bar:
        for weekdate in weekdates:
            #print('\nWEEKDATE',weekdate)
            for key in list(all_weeks[weekdate].keys()):
                #print('KEY',key,'\n',all_weeks[weekdate][key])
                k = key.lower()
                if not 'warm up' in k and not'warmup' in k and not 'class plan' in k and not 'workout brief' in k and not 'session' in k and not 'demo round' in k:
                    s = search(all_weeks[weekdate][key].lower(),movements,show=False)
                    s = create_values_string(s,all_weeks,weekdate,key)
                    insert_workout_table(os.getcwd()+"\\sugarwod_sql.db",all_columns,s)
                    #print(s)
                
                for move in movements[-8:]:
                    if search(k,[move],show=False)[0]:
                        #print('\n',key.lower())
                        #print('Move: ',move,'\nSearch: ',search(key.lower(),[move],show=False)[0])
                        check_name(os.getcwd()+"\\sugarwod_sql.db",move.split('/')[0],weekdate)
            bar.next()

        

if __name__ == '__main__':
    #sugarwod_table(reset = False)
    movements = []
    create_values_list(os.getcwd()+'\\movements.txt',movements)
    print(movements[-8:])
    s = search('asd dog sdf',['dog/ref'],show=True)
    t = 'dog/ref'.split('/')[0]
    print(t)

