import subprocess
import shutil
import glob
import os
import config
import datetime
import pandas as pd
import numpy as np

def format_date_for_row(d):
    row_date_temp = d.strftime('%x')
    if row_date_temp[0] == '0':
        row_date = row_date_temp[1:]
    else:
        row_date = row_date_temp
        
    return row_date

def download_files():
    print('New Johns Hopkins COVID-19 Files Download')
    # first you have to run 
    #  $ git clone https://github.com/CSSEGISandData/COVID-19.git
    # then add the home path to your repos to the config.py file

    # update local repo
    subprocess.call('cd ' + config.config['HOME_DIRECTORY'] + '/COVID-19; git pull origin master', shell=True)

    # copy file to my repo for processing
    print('Copying Files')
    
    #  get all daily files
    list_of_files = glob.glob(config.config['HOME_DIRECTORY'] + '/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv') 
    
    # copy to my repo
    for the_file in list_of_files:        
        shutil.copy(the_file, config.config['HOME_DIRECTORY'] + '/covid-19-usa-by-state/data/')
    
    print('New NYT data download')
    # update local repo
    subprocess.call('cd ' + config.config['HOME_DIRECTORY'] + '/covid-19-data; git pull origin master', shell=True)

    # copy file to my repo for processing
    print('Copying File')
    shutil.copy(config.config['HOME_DIRECTORY'] + '/covid-19-data/us-counties.csv', config.config['HOME_DIRECTORY'] +'/covid-19-usa-by-state/data/')
    
    return datetime.datetime.now()

def process_county_data():
    print('processing county data')
    # configuration
    datafile = './data/us-counties.csv'
    cases_save_file = 'COVID-19-Cases-USA-By-County.csv'
    deaths_save_file = 'COVID-19-Deaths-USA-By-County.csv'

    # load nyt county file
    df = pd.read_csv(datafile, encoding='utf-8', index_col=False)

    # process cases 
    df_cases = df.groupby(['date', 'fips', 'state', 'county']).agg({'cases':'sum'})
    
    # pivot cases table
    df_cases = df_cases.reset_index().pivot_table(index=['fips','state', 'county'], columns='date', values='cases',  aggfunc=sum,  margins=True, fill_value=0)

    # process deaths 
    df_deaths = df.groupby(['date', 'fips', 'state', 'county']).agg({'deaths':'sum'})

    # pivot deaths table
    df_deaths = df_deaths.reset_index().pivot_table(index=['fips','state', 'county'], columns='date', values='deaths',  aggfunc=sum,  margins=True, fill_value=0)

    # save tables to files
    df_cases.to_csv(cases_save_file, encoding='utf-8')
    df_deaths.to_csv(deaths_save_file, encoding='utf-8')

def process_states_data():       
    print('processing state data')
    # configuration
    data_folder = './data/'
    start_date = datetime.datetime(2020, 3, 22) # this is the date JH daily files were in the correct format for processing
    today_date = datetime.datetime.now()
    cases_datafile = 'COVID-19-Cases-USA-By-State.csv'
    cases_starter_datefile = data_folder + 'COVID-19-Cases-USA-By-State-Starter.csv'
    death_datafile = 'COVID-19-Deaths-USA-By-State.csv'
    death_starter_datefile = data_folder + 'COVID-19-Deaths-USA-By-State-Starter.csv'
  
    # load cases starter file
    df_cases = pd.read_csv(cases_starter_datefile, encoding='utf-8', index_col='State')
    # load deaths starter file
    df_deaths = pd.read_csv(death_starter_datefile, encoding='utf-8', index_col='State')

    while start_date <= today_date:
        file_date = start_date.strftime('%m-%d-%Y')    
        daily_date = format_date_for_row(start_date)
        daily_datafile = data_folder + file_date + '.csv'
        print(start_date)
        # load JH state files
        df = pd.read_csv(daily_datafile, encoding='utf-8', index_col=False)

        # filter only US rows
        df = df[df['Country_Region'] == 'US']

        # group by state
        df_daily_sum = df.groupby('Province_State').agg({'Confirmed':'sum','Deaths':'sum','Recovered':'sum'})

        # drop unneeded rows
        if 'Wuhan Evacuee' in df.index:
            df_daily_sum = df_daily_sum.drop(['Wuhan Evacuee'])
        if 'Recovered' in df.index:
            df_daily_sum = df_daily_sum.drop(['Recovered'])

        # get cases
        df_daily_cases = df_daily_sum.iloc[:, [0]]

        # get deaths
        df_daily_deaths = df_daily_sum.iloc[:, [1]]
    
        # insert empty column for current date into summary file
        dft = pd.DataFrame({ daily_date :  np.array([0] * df_cases.shape[0], dtype='int32'), })
        df_cases.insert(df_cases.shape[1], daily_date, dft.values)

        # insert cases into summary df
        for index, row in df_daily_cases.iterrows():    
            if index in df_cases.index:
                df_cases.at[index, daily_date] = row['Confirmed']  
    
        # insert empty column for current date into summary file
        dft = pd.DataFrame({ daily_date :  np.array([0] * df_deaths.shape[0], dtype='int32'), })
        df_deaths.insert(df_deaths.shape[1], daily_date, dft.values)    

        # insert deaths into summary df
        for index, row in df_daily_deaths.iterrows():    
            if index in df_deaths.index:
                df_deaths.at[index, daily_date] = row['Deaths']   

        start_date += datetime.timedelta(days=1)
            
    # save files
    df_deaths.to_csv(death_datafile, encoding='utf-8')
    df_cases.to_csv(cases_datafile, encoding='utf-8')

def commit_to_repo(process_date):
    print('committing to repo')
    subprocess.call(f'git commit -a -m "{process_date} data update"; git push origin master', shell=True)

def command_verification(command):
    print('please review following commands')
    print(command)
    result = input('Press ENTER to start: (type no to stop) ')
    if result == 'no':
        return False
    else:
        return True

def main():        
    process_date = download_files()   
    if command_verification("Process the files?"):
        process_county_data()
        process_states_data()
        if command_verification("Commit to Repo?"):
            commit_to_repo(process_date)
    print('finished')

if __name__ == "__main__":
    main()