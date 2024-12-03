from flask import Flask, jsonify
import requests
import json
import os
from bson.json_util import dumps
from match_parser import MatchDataParser
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# global variables
global player_collection

# local variables:

# riot api key
API_KEY = 'RGAPI-cab2fec5-ab41-4a13-b681-8b15c26a1328'

# base urls for riot api
ACCOUNT_BASE_URL = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
MATCH_BASE_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid"
MATCH_DETAIL_URL = "https://americas.api.riotgames.com/lol/match/v5/matches"

# load environment variables from .env file
load_dotenv()

# create flask app
app = Flask(__name__)

# retrieve mongo uri from .env file
uri = os.getenv("MONGO_URI")
if not uri:
    raise ValueError("MONGO_URI is not set in .env file")

# connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))

# check connection
try: 
    client.admin.command('ping')
    print("Pinging your deployment: You successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")



@app.route('/api/last-game/<game_name>/<tag_line>', methods=['GET'])
def get_last_game(game_name, tag_line):
    """
    Fetches the most recent match data for a given summoner by their Riot ID
    and writes it to a JSON file.

    Args:
        game_name (str): The summoner's game name.
        tag_line (str): The summoner's tag line.

    Returns:
        JSON response with the match data or an error message.
    """
    try:
        # Step 1: Get PUUID for the summoner
        account_url = f"{ACCOUNT_BASE_URL}/{game_name}/{tag_line}"
        headers = {"X-Riot-Token": API_KEY}
        account_response = requests.get(account_url, headers=headers)
        account_response.raise_for_status()
        account_data = account_response.json()
        puuid = account_data["puuid"]

        # Step 2: Get recent match ID for the summoner
        match_ids_url = f"{MATCH_BASE_URL}/{puuid}/ids?start=0&count=1"
        match_ids_response = requests.get(match_ids_url, headers=headers)
        match_ids_response.raise_for_status()
        match_ids = match_ids_response.json()

        if not match_ids:
            return jsonify({"error": "No recent matches found for the summoner."}), 404

        match_id = match_ids[0]

        # Step 3: Get match details for the match ID
        match_detail_url = f"{MATCH_DETAIL_URL}/{match_id}"
        match_detail_response = requests.get(match_detail_url, headers=headers)
        match_detail_response.raise_for_status()
        match_data = match_detail_response.json()

        # Step 4: Write match data to a JSON file
        output_file = f"last_game_{game_name}_{tag_line}.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(match_data, file, indent=4)
        print(f"Match data written to {output_file}")

        return jsonify({"message": f"Match data saved to {output_file}"})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": f"Key error: {e}"}), 500


@app.route('/api/parse-match/<game_name>/<tag_line>', methods=['GET'])
def parse_match(game_name, tag_line):
    """
    Parses the match JSON file for specific information and returns it.

    Args:
        game_name (str): The summoner's game name.
        tag_line (str): The summoner's tag line.

    Returns:
        JSON: Parsed match information.
    """
    file_path = f"last_game_{game_name}_{tag_line}.json"

    try:
        # Initialize the parser
        parser = MatchDataParser(file_path)

        # Extract data
        game_duration = parser.get_game_duration()
        match_participants = parser.get_all_participants()

        return jsonify({
            "gameDuration": game_duration,
            "matchParticipants": match_participants
        })
    except (FileNotFoundError, ValueError) as e:
        return jsonify({"error": str(e)}), 500

# Route to get all players from the mongo DB
@app.route('/api/players', methods=['GET'])
def get_all_players():
    """
    API endpoint to get all participants played with from MongoDB
    Args:
        game_name (str): Summoner's game name.
        tag_line (str): Summoner's tag line.
    Returns:
        JSON response with a list of participants or an error message.
    """
    try:
        mongo_collection = client["everything-league"]["summoners"]

        player_cursor = mongo_collection.find({}, {"_id": 0, "summonerName": 1})


        player_list = [player["summonerName"] for player in player_cursor]
        print(f'Player List: {player_list}')
        return jsonify({"players": player_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

@app.route('/api/add-players/<game_name>/<tag_line>', methods=['POST'])
def add_players(game_name, tag_line):
    """
    API endpoint to add participants to MongoDB.
    Expects a JSON payload containing the participants.

    Request Body:
    {
        "participants": ["Player1", "Player2", ...]
    }

    Returns:
        JSON response with a list of added participants or an error message.
    """
    file_path = f"last_game_{game_name}_{tag_line}.json"  # Path to the match JSON file
    try:
        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_path}"}), 404
        
        print(f"Received request to add participants for game_name={game_name}, tag_line={tag_line}")
        print(f"File path: {file_path}")

        # Initialize the parser
        parser = MatchDataParser(file_path)

        # Get all participants
        players = parser.get_all_players()
        print(f"Players fetched: {players}")

        # Reference the MongoDB collection
        mongo_collection = client["everything-league"]["summoners"]

        # Add each participant to the database
        added_players = []
        for player in players:
            # Insert participant into MongoDB if not already present
            result = mongo_collection.update_one(
                {"summonerName": player},
                {"$setOnInsert": {"summonerName": player, "stats": {}}},  # Placeholder stats
                upsert=True
            )
            if result.upserted_id:  # Only add if it was newly inserted
                added_players.append(player)

        print(f"Added players: {added_players}")
        return jsonify({
            "message": "Participants added to the database",
            "addedPlayers": added_players
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete-player/<player_name>', methods=['DELETE'])
def delete_player(player_name: str):
    """
    API endpoint to delete a player from the collection

    request_body:
    {
        "player_name": str
    }

    returns:
    JSON response letting the user know if the player was deleted if an error occurred
    """
    try:
        # reference the mongo collection
        mongo_collection = client["everything-league"]["summoners"]

        player_to_delete = mongo_collection.find_one_and_delete({"summonerName": player_name})

        if player_to_delete:
            return jsonify({
                "message": "Summoner deleted successfully",
                "summoner": dumps(player_to_delete)
            }), 200
        else:
            return jsonify({"error": f"Summoner {player_name} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
