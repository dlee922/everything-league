# Player data management
from flask import jsonify, current_app
from bson.json_util import dumps
import os
from parsers.match_parser import MatchDataParser

def get_all_players():
    try:
        # MongoDB collection reference
        mongo_collection = current_app.mongo_client["everything-league"]["summoners"]

        player_cursor = mongo_collection.find({}, {"_id": 0, "summonerName": 1})

        player_list = [player["summonerName"] for player in player_cursor]
        print(f'Player List: {player_list}')
        return jsonify({"players": player_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        mongo_collection = current_app.mongo_client["everything-league"]["summoners"]

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

def delete_player(player_name):
    try:
        mongo_collection = current_app.mongo_client["everything-league"]["summoners"]
        player = mongo_collection.find_one_and_delete({"summonerName": player_name})

        if player:
            return jsonify({"message": "Player deleted", "summoner": dumps(player)})
        else:
            return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500