# SOLUTION - CHALLENGE 1

First of all, we need to create a API connection to Bitso environment. To complete this task, it did exactly what is described in the official Bitso docs, which took some time to configure as well, but the API key and authentication were successfully created, as we can see in the image below:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/7a369379-b35d-4266-b197-e4141692a2ec)

Once the Bitso API has been created, to capture the data and calculate the order book spread, we must connect to the API using the generated key and secret. In this project, we will use Airflow to orchestrate the entire flow. Then, we will create a DAG that will automatically, given the necessary parameters, connect to the Bitso API, extract and transform the data and finally, will laod the data **already partitioned by datetime**, in .csv format in a folder that simulates (we can also compare) to an AWS S3 bucket. Remembering that the data will be loaded every 10 minutes divided by the load time, thus making it easier for analysts to use the data in the Data Lake and be able to monitor the oscillations of the spreads in a continuous and organized way. So, let's code!

## THE PIPELINE

To write our Airflow DAG, we should import some packages and define the arguments to go through. All the arguments written down below can be flexible, in this case, we have defined that que job will run every, every 10 minutes.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/46bd9871-c818-4a83-b9b7-45f25f3c3ef3)

Now, we will define a ETL function in Python. The function will connect to the Bitso API using key and secret created earlier and with these parameters, it will create a authentication to be able to acess the data. The code is right here:

```python
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
```

With the success of the API authorization, we already have the data recorded in a 'dictView' file. Now let's use more code to transform the extracted data into a .json output.


``` python
    # Transform the file extracted in a json file
    my_json = bitso.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    n_data = data["payload"]

    users_table = fromdicts(n_data)
```

Doing some transformations, our final goal is to obtain a dataframe to be easier to read.

``` python
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
```


Finally, we load the data into an already partitioned .csv file.

``` python
# Load the data into a CSV file

 df.to_csv(str(datetime.utcnow().strftime("%H:%M")) + bitso_data + "_data.csv", header = True, index=False)
```


Our ETL function was successfully built in python to capture the data!

Hence, we will finalize the DAG, scheduling it to perform the steps in "PythonOperator" every 10 minutes and we will use the "BashOperator" operator to create our Data Lake and move the data into it. We will end up with something similar to this.

``` python

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


```

**NOTE:** In the "Task 0", we've created a folder utilizing the function 'str(date.today())'. It will create a folder which the name of it is the today's date. Here, we emphasize that the name of our Data Lake can be any name that you want, it's not a rule! Just change this part of the code. 

**NOTE:** The parameter 'schedule=timedelta(minutes=10)' on the DAG argument it is who defines how often the job will run, in our case, every 10 minutes.

Then, Workflow should be like:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/d4f7d0f5-5208-4416-814f-109383b68873)

## RESULTS

Let's trigger the DAG in Airflow environment. First of all, we need to remember to activate our Airflow web server and Scheduler by writing in the terminal the following codes:


```python
airflow webserver -p 8080
```

```python
airflow scheduler
```

With our DAG on the Scheduler Screen, we can trigger it and see the results. The image below shows what exactly happens:


![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/08d64ab1-024c-48f0-a095-cd5a1e95ac67)

In the Data Lake directory, we can see the data partitioned by datetime, every 10 minutes creates a new file .csv. This type of partition, in addition to being the most common and simplest, can facilitate the ingestion of data from a Data Warehouse or Data Mart into AWS S3 using AWS Glue and AWS Athena to catalog the data or unite all the tables by creating a single table, for example. Both the Data Engineer and the Data Scientist can work quickly in a variety of ways with this partitioned data.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/5949bab0-6d05-4812-abd4-fb8e81f9ece8)


![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/6c286b64-820f-4b1b-995e-bfc4c4cd451b)


### Some examples of the output partitioned data of this project is attached in the Challenge_1 folder.
