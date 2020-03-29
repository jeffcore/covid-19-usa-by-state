# COVID-19

COVID-19 data USA States by day. All data from Johns Hopkins https://coronavirus.jhu.edu

The raw data from Johns Hopkins is organized by county, state, country. Also each day is a new file. This repo takes the  
daily files and combines all the data into two csv files (confirmed cases and deaths). Daily data is accumulated, not new cases/deaths per day.  

Rows: State Name  
Columns: Date  

Last Updated: 3/27/20

## Files

1. COVID-19-Confirmed-Cases-USA-By-State.csv - CSV file of daily total confirmed cases in the USA by state.
2. COVID-19-Deaths-USA-By-State.csv - CSV file of and daily total confirmed deaths in the USA by state.
3. Daily-Total-Cases-Data-Process.ipynb - python notebook for processing Johns Hopkins daily files into aggregated file.
4. Daily-Total-Deaths-Data-Process.ipynb - python notebook for processing Johns Hopkins daily files into aggregated file.
5. download-jh-data.py - python script to automate downloading the daily file from the John Hopkins repo.  
