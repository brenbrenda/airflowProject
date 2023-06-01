
def fetch_data_from_twitter(kwargs):
    print("We are getting data from ")
    print("----------")
    print("======done!======")


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