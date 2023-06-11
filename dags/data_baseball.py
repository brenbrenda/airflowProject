from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import requests
import json
import http.client

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to fetch data from API


# Function to load data to Elasticsearch
def load_data_to_es(index_name, **context):
    password = os.environ["ENV_PASSWORD"]
    user = 'elastic'
    es_instance = Elasticsearch(
        ['baseball.es.us-central1.gcp.cloud.es.io:9243'],
        http_auth=(user, password),
        scheme="https",
    )
    data1 = context['ti'].xcom_pull(task_ids='fetch_data_from_api_1')
    es_instance.index(index=index_name, body={'data': data1})
def store_player_teams_to_es():
    es = Elasticsearch("https://elastic:XJO0NIuus6ovQxGGH5axO49x@baseball.es.us-central1.gcp.cloud.es.io:9243")
    player_teams_data = get_baseball_data()  # Assume this function fetches the data shown in your question

    for player_team in player_teams_data["player_teams"]["queryResults"]["row"]:
        player_team_data = {
            "player_id": player_team["player_id"],
            "team_name": player_team["team"],
            "league": player_team["league"],
            "start_date": player_team["start_date"],
            "end_date": player_team["end_date"],
            "status": player_team["status"],
            # Add more fields as needed
        }
        es.index(index="player_teams", body=player_team_data)


def getplayerMatchesData():
    conn = http.client.HTTPSConnection("baseballapi.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        'X-RapidAPI-Host': "baseballapi.p.rapidapi.com"
    }

    conn.request("GET", "/api/baseball/player/977489/matches/near", headers=headers)

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
    print(data)


def getplayernearMatch():
    conn = http.client.HTTPSConnection("baseballapi.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        'X-RapidAPI-Host': "baseballapi.p.rapidapi.com"
    }

    conn.request("GET", "/api/baseball/player/977489/tournament/11205/season/29168/statistics/regularSeason",
                 headers=headers)

    res = conn.getresponse()

    data = res.read()
    return data.decode("utf-8")


def fetch_playerdata():
    # Set the parameters
    game_type = "'R'"
    season = "'2017'"
    player_id = "'493316'"

    # Construct the endpoint URL
    endpoint_url = f"http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type={game_type}&season={season}&player_id={player_id}"

    try:

        response = requests.get(endpoint_url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


import http.client
import json
from elasticsearch import Elasticsearch


def get_player_matches(player_id):
    try:
        endpoint_url = f"http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{player_id}'"
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))


def store_matches_to_es(data):
    if data is not None:
        # Parse JSON data
        player_info = data['player_info']['queryResults']['row']

        # Extract desired information
        player_data = {
            "gender": player_info['gender'],
            "name": player_info['name_display_first_last'],
            "position": player_info['primary_position_txt'],
            "age": player_info['age'],
            "primary_stat_type": player_info['primary_stat_type'],
            "height_feet": player_info['height_feet'],
            "height_inches": player_info['height_inches'],
            "weight": player_info['weight']
        }

        # Store data to Elasticsearch
        es = Elasticsearch("https://elastic:XJO0NIuus6ovQxGGH5axO49x@baseball.es.us-central1.gcp.cloud.es.io:9243")
        es.index(index="players", document=player_data)


def getplayerMatchesData():
    url = "https://baseballapi.p.rapidapi.com/api/baseball/match/9864379/statistics"

    headers = {
        "X-RapidAPI-Key": "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        "X-RapidAPI-Host": "baseballapi.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    return data.decode("utf-8")





def getnearMatch():
    url = "https://baseballapi.p.rapidapi.com/api/baseball/player/977489/matches/near"

    headers = {
        "X-RapidAPI-Key": "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        "X-RapidAPI-Host": "baseballapi.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(response.json())
    return data


def store_statistics_to_es(**context):
    data = context['ti'].xcom_pull(task_ids='get_player_match_data')

    es = Elasticsearch("https://elastic:XJO0NIuus6ovQxGGH5axO49x@baseball.es.us-central1.gcp.cloud.es.io:9243")

    for group in data["statistics"][0]["groups"]:
        for item in group["statisticsItems"]:
            stats_data = {
                "groupName": group["groupName"],
                "name": item["name"],
                "away": item["away"],
                "home": item["home"],
                "compareCode": item["compareCode"]
            }
            es.index(index="statistics", document=stats_data)


def hivetoMAtch():
    url = "https://baseballapi.p.rapidapi.com/api/baseball/match/ExbsIxb/h2h"

    headers = {
        "X-RapidAPI-Key": "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        "X-RapidAPI-Host": "baseballapi.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(response.json())
    return data


def hiveUploadEs(matches):
    #     matches = json.loads(string)
    es = Elasticsearch("https://elastic:XJO0NIuus6ovQxGGH5axO49x@baseball.es.us-central1.gcp.cloud.es.io:9243")
    for match in matches['events']:
        match_data = {
            #         "match_id": match["id"],
            "away_team": match["awayTeam"],
            "home_team": match["homeTeam"],
            "status": match["status"],
            "tournament": match["tournament"],
            "start_timestamp": match["startTimestamp"]
        }
        es.index(index="matchhive", document=match_data)



with DAG('baseball_statistic', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    headers = {
        "X-RapidAPI-Key": "07fdb96e40msh53a760439ea7517p18f3abjsn37b9863a67b5",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    player_id = "493316"
    params = {"playerId": player_id, "statType": "stolenBase"}
    t1 = PythonOperator(
        task_id='get_player_match_data',
        python_callable=getplayerMatchesData,
        provide_context=True,
        dag=dag)

    t2 = PythonOperator(
        task_id='store_statistics_to_es',
        python_callable=store_statistics_to_es,
        provide_context=True,
        dag=dag)

    t3 = PythonOperator(
        task_id='hive_to_match',
        python_callable=hivetoMAtch,
        dag=dag
    )

    t4 = PythonOperator(
        task_id='hive_upload_es',
        python_callable=hiveUploadEs,
        provide_context=True,
        dag=dag)

    t1 >> t2
    t2 >> t3
    t3 >> t4
