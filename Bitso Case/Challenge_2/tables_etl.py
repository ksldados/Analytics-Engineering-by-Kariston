from datetime import datetime
import json
from pandas import json_normalize
import sqlite3
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor

default_args = {
    'start_date': datetime(2023, 9, 1)
}


with DAG('tables_etl', schedule_interval='@daily',
        default_args=default_args,
        catchup=False) as dag:
        
        # Define tasks/operators
        
    ct1 = SqliteOperator(
        task_id='creating_table_deposits',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS deposits (
		        id INTEGER NOT NULL UNIQUE,
		        event_timestamp TEXT NOT NULL,
		        user_id TEXT NOT NULL,
		        amount REAL NOT NULL,
		        currency TEXT NOT NULL,
		        tx_status TEXT NOT NULL
		    );
	''' 
    )
    
    ct2 = SqliteOperator(
        task_id='creating_table_front_events',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS front_events (
		        id INTEGER NOT NULL UNIQUE,
		        event_timestamp TEXT NOT NULL,
		        user_id TEXT NOT NULL,
		        event_name TEXT NOT NULL
		    );
	''' 
    )
    
    ct3 = SqliteOperator(
        task_id='creating_table_withdrawals',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS withdrawals (
		        id INTEGER NOT NULL UNIQUE,
		        event_timestamp TEXT NOT NULL,
		        user_id TEXT NOT NULL,
		        amount REAL NOT NULL,
		        interface TEXT NOT NULL,
		        currency TEXT NOT NULL,
		        tx_status TEXT NOT NULL
		    );
	''' 
    )
    
  
    
    storing_data1 = BashOperator(
        task_id='storing_data_deposits',
        bash_command='echo -e ".separator ","\n.import /home/kariston/datalake_bitso/deposit_sample_data.csv deposits" | sqlite3 /home/kariston/bitso_database.db'
    )
    
    storing_data2 = BashOperator(
        task_id='storing_data_front_events',
        bash_command='echo -e ".separator ","\n.import /home/kariston/datalake_bitso/event_sample_data.csv front_events" | sqlite3 /home/kariston/bitso_database.db'
    )
    
    storing_data3 = BashOperator(
        task_id='storing_data_withdrawals',
        bash_command='echo -e ".separator ","\n.import /home/kariston/datalake_bitso/withdrawals_sample_data.csv withdrawals" | sqlite3 /home/kariston/bitso_database.db'
    )
            
#Workflow    
ct1 >> storing_data1
ct2 >> storing_data2
ct3 >> storing_data3	    



