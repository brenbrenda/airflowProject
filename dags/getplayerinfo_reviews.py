import requests
def get_player_info_and_reviews(player_id, review_count=5):
    # Define the base URL for the MLB lookup service API
    base_url = "http://lookup-service-prod.mlb.com"

    # Create the URL for the specific player
    player_url = f"{base_url}/json/named.player_info.bam"
    # Define parameters
    params = {"player_id": player_id, "sport_code": "'mlb'"}

    # Send a GET request to the MLB lookup service API for the player info
    player_response = requests.get(player_url, params=params)

    # If the GET request is successful, the status code will be 200
    if player_response.status_code == 200:
        # Get the JSON data from the response
        player_data = player_response.json()

        # Access the 'player_info' field in the response
        player_info = player_data["player_info"]["queryResults"]["row"]

        # Print the name, type, game history, score, and popularity of the player
        print(f"Name: {player_info['name_display_first_last']}")
        print(f"Team: {player_info['team_name']}")
        print(f"Bats: {player_info['bats']}")
        print(f"Throws: {player_info['throws']}")

    # Assuming there's another endpoint to get reviews about the player
    review_url = f"{base_url}/json/named.player_reviews.bam"

    # Send a GET request to the MLB lookup service API for the player reviews
    review_response = requests.get(review_url, params={"player_id": player_id})

    # If the GET request is successful, the status code will be 200
    if review_response.status_code == 200:
        # Get the JSON data from the response
        review_data = review_response.json()

        # Access the 'reviews' field in the response
        reviews = review_data["reviews"]["queryResults"]["row"]

        # Limit the number of reviews to the specified review count
        reviews = reviews[:review_count]

        # Iterate over each review
        for review in reviews:
            # Print the username of the reviewer and the review text
            print(f"\nReviewer: {review['reviewer']}")
            print(f"Review: {review['text']}")
            print(f"Date: {review['date']}")
            # Test the function with a player ID
            get_player_info_and_reviews("605141")

