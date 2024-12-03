# Match fetching and parsing logic
from flask import jsonify
import os
import json
import requests
from parsers.match_parser import MatchDataParser

def fetch_last_game(game_name, tag_line):
    try:
        # Add logic from `get_last_game` function in app.py
        pass
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_match_data(game_name, tag_line):
    try:
        file_path = f"last_game_{game_name}_{tag_line}.json"
        parser = MatchDataParser(file_path)

        # Extract and return parsed data
        return jsonify({
            "gameDuration": parser.get_game_duration(),
            "matchParticipants": parser.get_all_players()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500