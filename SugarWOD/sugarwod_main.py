# ====== MAIN ====== #
# Runs Sugarwod scripts

# ====== IMPROVEMENTS ====== #
# 

from sugarwod_scrape_v1 import *
from sugarwod_parse import *
from sugarwod_table import *

# === RESET PARAMETER === #
resetvar = False

if __name__ == '__main__':

    print('\n=============== SUGARDWOD STARTED ===============')
    if resetvar:
        invar = input('\nReset json/table selected. This will rewrite .json file and recreate .db file.\n\nContinue? [Y/N] ')
        if invar.lower() == 'y':
            print('\nReset started...\n')
        else:
            print('\nTerminated.\n')
            quit()

    scrape_dates = sugarwod_scrape_v1()  
    sugarwod_parse(scrape_dates, reset = resetvar)
    sugarwod_table(scrape_dates, reset = resetvar)

    print('\n============= SUGARWOD DATABASE UPDATED =============\n')