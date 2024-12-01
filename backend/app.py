from flask import Flask, jsonify
import requests
import json
import os
from match_parser import MatchDataParser

app = Flask(__name__)

# Your Riot API key
API_KEY = 'RGAPI-c7b400ed-c4e8-4339-9cd2-940024de1c89'

# Base URLs for Riot API
ACCOUNT_BASE_URL = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
MATCH_BASE_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid"
MATCH_DETAIL_URL = "https://americas.api.riotgames.com/lol/match/v5/matches"


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
    
# Route to get all participants from a specific match JSON file
@app.route('/api/participants/<game_name>/<tag_line>', methods=['GET'])
def get_all_participants(game_name, tag_line):
    """
    API endpoint to get all participants in a match.
    Args:
        game_name (str): Summoner's game name.
        tag_line (str): Summoner's tag line.
    Returns:
        JSON response with a list of participants or an error message.
    """
    file_path = f"last_game_{game_name}_{tag_line}.json"  # Path to the match JSON file

    try:
        # Initialize the parser
        parser = MatchDataParser(file_path)

        # Get all participants
        participants = parser.get_all_participants()

        return jsonify({"participants": participants})

    except (FileNotFoundError, ValueError) as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    app.run(debug=True)
