# SOLUTION - CHALLENGE 1

First of all, we need to create a API connection to Bitso environment. To complete this task, it did exactly what is described in the official Bitso docs, which took some time to configure as well, but the API key and authentication were successfully created, as we can see in the image bellow:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/7a369379-b35d-4266-b197-e4141692a2ec)

Once the Bitso API has been created, to capture the data and calculate the order book spread, we must connect to the API using the generated key and secret. In this project, we will use Airflow to orchestrate the entire flow. Then, we will create a DAG that will automatically, given the necessary parameters, connect to the Bitso API, extract and transform the data and finally, will laod the data **already partitioned by datetime**, in .csv format in a folder that simulates (we can also compare) to an AWS S3 bucket. Remembering that the data will be loaded every 10 minutes divided by the load time, thus making it easier for analysts to use the data in the Data Lake and be able to monitor the oscillations of the spreads in a continuous and organized way. So, let's code!

## THE PIPELINE

To write our Airflow DAG, we should import some packages and define the arguments to go through. All the arguments written down bellow can be flexible, in this case, we have defined that que job will run every, every 10 minutes.

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
