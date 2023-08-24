# Project - Web Scraping and ETL with Airflow to Calculate the Spread of Shares on the Stock Exchange

Let's build a data pipeline with Apache Airflow. 
In this project our goal will be to build an ETL process to extract data from the web by using web scraping technique, organize and transform the data, calculate the spread (we will work with financial data) and then generate the output. 
All this will be done automatically with Airflow.

# Starting the Project

A recommendation for this project is to carry it out in a Linux environment in order to make it easier for the user.
After configuring a computer with OS Linux or a virtual environment, we will proceed to install Apache Airflow on the local computer.

To install the Apache Airflow, just type the following command on your terminal: 

```python
pip install apache-airflow
```

Having done the previous step, now we must initialize SQLite for Airflow to work properly. To do so, just type the following code:

```python
airflow db init
```
And then, we can initialize Apache Airflow on our own PC:

```python
airflow webserver -p 8080
```

Now we create admin user for SQLite Database on Airflow doing this:

```python
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
```
Finally, start the Airflow Scheduler:

```python
airflow scheduler
```
Done! Your Apache Airflow environment has been created. A folder named "Airflow" also has been created on your user space. Firstly, you need to confiure de "airflow.cfg" inside this folder and put your code's folder in the path, something like this:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/e25dcce9-030e-48f4-a989-b78563458546)

All your DAG codes must be in this path to work correctly.

## Web Scraping and ETL with Airflow to Calculate the Spread of Shares on the Stock Exchange

Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. Airflow’s extensible Python framework enables you to build workflows connecting with virtually any technology. A web interface helps manage the state of your workflows. Airflow is deployable in many ways, varying from a single process on your laptop to a distributed setup to support even the biggest workflows.

We gonna program a Daily Airflow Scheduler Job (DAG) written in Python Language of a ETL process of the Shares on the Stock Exchange data of the Apple and Tesla Companies.

In this moment, we must create our own scheduler code to perform Extraction of our Stock Exchange Data, put into this code some transformations to calculate the Spread of the Shares and finally, we need to choose where the data will be loaded.

The code containing this job can be seen in the attached project folder named 'daily_spread_etl_job.py'. To run this DAG on the Airflow screen, you need to navigate through your terminal to the folder where the DAG code is in (the folder that you set up before on airflow.cfg) and in your terminal screen type something like this (but using your own path): 


```terminal
~/home/dmpm/DAG$ python daily_spread_etl_job.py 
```
No errors should appear and then, your DAG must be shown on Airflow environment when you access using your browser using localhost.

Finally, running the DAG, on monitoring screen in Airflow, we should have something similar to this image:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/ef9cc91c-9083-4059-9383-dd399312b985)
