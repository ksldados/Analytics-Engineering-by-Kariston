# SOLUTION - CHALLENGE 2 

In this solution, we will use Airflow to orchestrate the data pipeline to create tables and load them to a SQLite database. 
First, we gonna use the following data model shown below:

![data_model](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/193505e8-dbf5-4860-acdb-45749e80d1d1)


In this case, we will use only 3 CSV files out of the 4 provided in this challenge, as we understand that it will facilitate obtaining the results. 

Hence, the CSV files used in this pipeline will be attached in this GIT project.

Let's start code our DAG file to orchestrate the role pipeline. First of all, we need to activate our Airflow webs server and  Scheduler by writing in the terminal the following codes:


```python
airflow webserver -p 8080
```

```python
airflow scheduler
```

First, let's create a database in SQLite3, for that, let's use the command in a terminal window:

```python
sqlite3 bitso_database.db
```
To verify that we created it successfully, just type the command below and our data base should appear.

```python
.databases
```

Now, open the Airflow on browser (usually located at http://0.0.0.0:8080/home) and let's set up a connection with the SQLite Database. To do so, after opening Airflow, click on Admin > Connections at the top of the screen.
A screen similar to the image below should open. Then, click on the "+" icon.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/0048e901-ef68-4b12-8070-71f2c7b0a76e)

Configure the connection to the SQLite database we created earlier. To do so, click on the "+" icon and fill in the fields as shown in the image below, changing only the directory where your db is created.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/9494fa0d-e5cc-4906-8c66-0d9a31e08860)

Done! Now we have our Database configured.

Now, we can create a python file and import some packages and define arguments to work our DAG file.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/dbcf6540-43f2-45d2-86c8-dfc136e16bdf)

For this example, let's set the DAG schedule run interval to 'daily'. Now, we gonna use the 'SqliteOperator' to create, using DDL, the tables in our SQLite database.
The tables will be created simultaneously as follows:

```python
with DAG('tables_etl', schedule_interval='@daily',

        default_args=default_args,

        catchup=False) as dag:

        

        # Define tasks/operators

        

    ct1 = SqliteOperator(

        task_id='creating_table_deposits',

        sqlite_conn_id='db_sqlite',

        sql='''

            CREATE TABLE IF NOT EXISTS deposits (

		        id INTEGER NOT NULL,

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

		        id INTEGER NOT NULL,

		        event_timestamp TEXT NOT NULL,

		        user_id TEXT NOT NULL PRIMARY KEY,

		        event_name TEXT NOT NULL

		    );

	''' 

    )

    

    ct3 = SqliteOperator(

        task_id='creating_table_withdrawals',

        sqlite_conn_id='db_sqlite',

        sql='''

            CREATE TABLE IF NOT EXISTS withdrawals (

		        id INTEGER NOT NULL,

		        event_timestamp TEXT NOT NULL,

		        user_id TEXT NOT NULL,

		        amount REAL NOT NULL,

		        interface TEXT NOT NULL,

		        currency TEXT NOT NULL,

		        tx_status TEXT NOT NULL

		    );

	''' 

    )
```
    
Finally, let's use 'BashOperator' to import our CSV files to the tables created earlier into our database. The code is written below.

```python
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
```

Hence, the workflow to run our DAG is:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/3f0754a6-3fed-4741-92e9-a166da755056)

Done! Our DAG is ready to be orchestrated! Now we have the following graph running successfully in Airflow:

![airflow_2](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/726498b6-0a16-4128-bd08-e7bffcaa7b9e)
