import subprocess
import shutil
import glob
import os
import config

print('New Johns Hopkins COVID-19 Files Download')
# first you have to run 
#  $ git clone https://github.com/CSSEGISandData/COVID-19.git
# then add the home path to your repos to the config.py file

# update local repo
subprocess.call('cd ' + config.config['HOME_DIRECTORY'] + '/COVID-19; git pull origin master', shell=True)

# get all daily files
list_of_files = glob.glob(config.config['HOME_DIRECTORY'] +'/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv') # * means all if need specific format then *.csv

# get lastest downloaded file
latest_file = max(list_of_files, key=os.path.getctime)
print('Lastest File: ' + latest_file)

# copy file to my repo for processing
print('Copying File')
shutil.copy(latest_file, config.config['HOME_DIRECTORY'] +'/covid-19-usa-by-state/data/')
   