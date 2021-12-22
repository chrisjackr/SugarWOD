# ====== MAIN ====== #
# Runs Sugarwod scripts

# ====== IMPROVEMENTS ====== #
# 

from sugarwod_scrape_v1 import *
from sugarwod_parse import *
from sugarwod_table import *

# === RESET PARAMETER === #
#resetvar = True

if __name__ == '__main__':

    print('\n=============== SUGARDWOD STARTED ===============')
    resetask = input('\nReset table? [Y/N] ')
    if resetask.lower() == 'y':
        resetvar = True
    else:
        resetvar = False
        
    if resetvar:
        invar = input('\nReset json/table selected. This will rewrite .json file and recreate .db file.\n\nContinue? [Y/N] ')
        if invar.lower() == 'y':
            print('\nReset started...\n')
        else:
            print('\nTerminated.\n')
            quit()

    print('CWD: ',os.getcwd())
    scrape_dates = sugarwod_scrape_v1()  
    sugarwod_parse(scrape_dates, reset = resetvar)
    sugarwod_table(scrape_dates, reset = resetvar)

    print('\n============= SUGARWOD DATABASE UPDATED =============\n')

    invar = input('\nShow generate dashboard in browser? [Y/N] ')
    if invar.lower() == 'y':
        import sugarwod_dashboard
        sugarwod_dashboard
    
    print('\nDashboard generated.\n')
    print('\n============= FINISH =============\n')




    