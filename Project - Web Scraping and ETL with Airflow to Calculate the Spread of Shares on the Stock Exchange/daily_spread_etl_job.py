# Obs: Change the path to save the files!

# pip install yfinance
# pip install simplejson

# Imports
import simplejson
import pandas as pd
import yfinance as yf
import datetime as dt
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import date, datetime, timedelta

# Arguments
default_args = {
    'owner': 'admin',
    # Put your initial date to start to collect the data
    'start_date': dt.datetime(2023,8,1), 
    'email': ['admin@admin.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': dt.timedelta(minutes = 5)
}

# Data download function
def download_stock_data(stock_ticker):

    # Data collection start date
    start_date = date.today()

    # End date of data collection
    end_date = start_date + timedelta(days = 1)

    # Data Download
    df = yf.download(stock_ticker, start = start_date, end = end_date, interval = '1m')

    # Generation of the csv file with the extracted data
    df.to_csv(stock_ticker + "_data.csv", header = True)

# Spread calculation function
def get_last_stock_spread():

    # Loads files into pandas dataframes
    apple_data = pd.read_csv("/Users/dmpm/Dropbox/Lab2/data/" + str(date.today()) + "/AAPL_data.csv") #Change to your own path here!
    tesla_data = pd.read_csv("/Users/dmpm/Dropbox/Lab2/data/" + str(date.today()) + "/TSLA_data.csv") #Change to your own path here!

    # Spread Calculation
    spread = [(apple_data['High'][0] + apple_data['Low'][0]) / 2, (tesla_data['High'][0] + tesla_data['Low'][0]) / 2]

    # Open the text file to load the spread
    f = open('spread.txt', 'w')

    # Dump the list (spread) on the file
    simplejson.dump(spread, f)

    # Close the file
    f.close()

# Create the DAG
# https://crontab.guru/
with DAG('lab2', default_args = default_args, schedule_interval = '45 18 * * 1-5', description = 'Spread Apple e Tesla') as dag:
 
    # Task 0
    t0 = BashOperator(task_id = 'Cria_Diretorio_Temporario',
                      bash_command = '''mkdir -p /Users/dmpm/Lab2/data/''' + str(date.today()), #Change to your own path here!
                      dag = dag)
    
    # Task 1
    t1 = PythonOperator(task_id = 'AAPL_stock_download',
                        python_callable = download_stock_data,
                        op_kwargs = {'stock_ticker': 'AAPL'},
                        dag = dag)

    # Task 2
    t2 = PythonOperator(task_id = 'TSLA_stock_download',
                        python_callable = download_stock_data,
                        op_kwargs = {'stock_ticker': 'TSLA'},
                        dag = dag)

    # Task 3
    t3 = BashOperator(task_id = 'Move_APPL_data',
                      bash_command = '''mv /Users/dmpm/AAPL_data.csv /Users/dmpm/Lab2/data/''' + str(date.today()) + '/', 
                      dag = dag) #Change to your own path here!

    # Task 4
    t4 = BashOperator(task_id = 'Move_TSLA_data',
                      bash_command = '''mv /Users/dmpm/AAPL_data.csv /Users/dmpm/Lab2/data/''' + str(date.today()) + '/',
                      dag = dag) #Change to your own path here!
    
    # Task 5
    t5 = PythonOperator(task_id = 'Calcula_Spread_Salva_Resultado',
                        python_callable = get_last_stock_spread,
                        dag = dag)

    # Task 6

    t6 = BashOperator(task_id = 'Move_Spread_data',

                      bash_command = 'mv /Users/dmpm/Lab2/data/spread.txt /Users/dmpm/Lab2/' + '/',

                      dag = dag)

# Workflow
t0 >> [t1, t2]
t3 << t1
t4 << t2
[t3,t4] >> t5 >> t6

