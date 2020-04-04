# COVID-19

COVID-19 data USA States by day. State data from Johns Hopkins https://coronavirus.jhu.edu . County Data from NYT https://github.com/nytimes/covid-19-data .

## State Data
The raw data from Johns Hopkins is organized by county, state, country. Also each day is a new file. This repo takes the  
daily files and combines all the data into two csv files (confirmed cases and deaths). Daily data is cumulative counts, not new cases/deaths per day.  

Rows: State Name  
Columns: Date  

## County Data
The raw data from NYT is organized by daily rows of date, county, state, values. This repo takes the  
daily data and combines all the data into two csv files (confirmed cases and deaths). Daily data is cumulative counts, not new cases/deaths per day.  

Rows: FIPS, County, State  
Columns: Date  

Last Updated: 4/3/20

## Files

1. COVID-19-Cases-USA-By-State.csv - CSV file of daily total confirmed cases in the USA by state.
2. COVID-19-Deaths-USA-By-State.csv - CSV file of and daily total confirmed deaths in the USA by state.
3. COVID-19-Cases-USA-By-County.csv - CSV file of daily total confirmed cases in the USA by county.
4. COVID-19-Deaths-USA-By-County.csv - CSV file of and daily total confirmed deaths in the USA by county.
5. Process-Daily-Files.ipynb - python notebook for processing Johns Hopkins daily files into aggregated files.
6. Process-NYT-File.ipynb - python notebook for processing NYT file into aggregated files.
7. download-jh-data.py - python script to automate downloading the daily file from the John Hopkins repo.  
