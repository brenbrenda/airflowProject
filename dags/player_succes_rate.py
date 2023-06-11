from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import requests
import json

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to fetch data from API
def fetch_data_from_api(endpoint, headers, params):
    response = requests.get(endpoint, headers=headers, params=params)
    data = response.json()
    return data

# Function to load data to Elasticsearch
def load_data_to_es(index_name, **context):
    password = os.environ["ENV_PASSWORD"]
    user = 'elastic'
    es_instance = Elasticsearch(
        ['my_elasticsearch_service_url'],
        http_auth=(user, password),
        scheme="https",
    )
    data1 = context['ti'].xcom_pull(task_ids='fetch_data_from_api_1')
    es_instance.index(index=index_name, body={'data': data1})


def fetch_data_from_baseball_fastApi():
    print("=== fetching baseball api ===")
    import json
    import requests

    # Fetch the data
    response = requests.get("https://api.yourapi.com/endpoint")
    data = response.json()

    # Write the data to a JSON file
    with open('basball.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_baseball_data():
    api_key = "YOUR_API_KEY"
    endpoint_url = "http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='493316'"
    player_id = "12345"
    params = {"playerId": player_id, "statType": "stolenBase"}

    response = requests.get(endpoint_url)

    if response.status_code == 200:
        data = response.json()
        stolen_bases = data
        print(stolen_bases)
    else:
        print("Error:", response.status_code)

with DAG('player_success_rate', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    headers = {
        "X-RapidAPI-Key": "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }
    params = {"all": "true"}

    t1 = PythonOperator(
        task_id='fetch_data_from_api_1',
        python_callable=fetch_data_from_baseball_fastApi,
        op_kwargs={
            'endpoint': 'https://odds.p.rapidapi.com/v4/sports',
            'headers': headers,
            'params': params
        },
        provide_context=True,
        dag=dag)


    t2 = PythonOperator(
        task_id='get_baseball_data_task',
        python_callable=get_baseball_data,
        dag=dag
    )

    t3 = PythonOperator(
        task_id='load_data_to_es',
        python_callable=load_data_to_es,
        op_kwargs={'index_name': 'player_data'},
        provide_context=True,
        dag=dag)

    t1 >> t3
    t2 >> t3

