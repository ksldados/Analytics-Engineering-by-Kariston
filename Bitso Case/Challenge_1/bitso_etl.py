# Imports
import simplejson
import pandas as pd
import time
import pendulum
import hmac
import hashlib
import requests
import json
import random
import sys
import os
import datetime as dt
import urllib.request, json
import urllib3
from petl import look, fromdb,fromjson,fromdicts,unpackdict,cut, todb, rename, tocsv
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import date, datetime, timedelta

# Arguments
default_args = {
    'owner': 'admin',
    'start_date': pendulum.datetime(2023, 9, 2, tz="UTC"),
    'email': ['admin@admin.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': dt.timedelta(minutes = 10)
}


# ETL function
def download_bitso_data(bitso_data):

    # Connect to the Bitso API using credentials created before
    bitso_url = "https://sandbox.bitso.com"
    bitso_key = "NTqJzgcrXd"
    bitso_secret = "12cef27c83c5f7b289e49964d08dab8d"
    nonce = str(int(round(time.time())) * 100000 * 2)
    http_method = "POST"
    request_path = "/api/v3/ticker/" 
    payload = {}
    # Add required keys of the parameters to the json
    json_payload = json.dumps(payload).encode('utf-8')
    # Create signature
    message = nonce + http_method + request_path + str(json_payload)
    signature = hmac.new(bitso_secret.encode('utf-8'),
		                message.encode('utf-8'),
		                hashlib.sha256).hexdigest()
    
    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://sandbox.bitso.com/api/v3/ticker/')
    bitso = r.data	
    
    # Transform the file extracted in a json file
    my_json = bitso.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    n_data = data["payload"]
    users_table = fromdicts(n_data)
    
    # Picking only specific columns
    users_table = cut(users_table, 'created_at','book','bid','ask')
    
    # Rename a column
    users_table = rename(users_table, {'created_at':'orderbook_timestamp'})
    df = users_table.todataframe()

    # Convert columns
    df['bid'] = df['bid'].astype(float)
    df['ask'] = df['ask'].astype(float)
    
    # Spread calculate
    spread = ((df['ask'] - df['bid'])*100 / df['ask'])
    
    # Put the Spread calculated into the dataset
    df['spread'] = spread
     
    # Convert more columns
    df['spread'] = df['spread'].astype(float)
    
    #Filtering only the right order books
    df = df.query("book in ('btc_mxn','usd_mxn')")
    
    # Load the data into a CSV file
    df.to_csv(str(datetime.utcnow().strftime("%H:%M")) + bitso_data + "_data.csv", header = True, index=False)

 
# Build the DAG

with DAG('bitso_etl', default_args = default_args, schedule=timedelta(minutes=10), description = 'Bitso ETL',catchup=False) as dag:

    # Task 0
    t0 = BashOperator(task_id = 'create_my_datalake',
                      bash_command = '''mkdir -p /home/kariston/test_zone/data/''' + str(date.today()) + '/',
                      dag = dag)
           
    # Task 1
    t1 = PythonOperator(task_id = 'download_bitso_data',
                        python_callable = download_bitso_data,
                        op_kwargs = {'bitso_data': 'bitso'},
                        dag = dag)

    # Task 2
    t2 = BashOperator(task_id = 'move_bitso_data',
                      bash_command = 'mv /home/kariston/'+ str(datetime.utcnow().strftime("%H:%M")) + 'bitso_data.csv /home/kariston/test_zone/data/' + str(date.today()) + '/',
                      dag = dag)

 
# Workflow
t0 >> t1 >> t2


