# Routes for fetching and parsing match data
from flask import Blueprint, jsonify, request
from app.services.match_service import fetch_last_game, parse_match_data

match_bp = Blueprint('match', __name__)

@match_bp.route('/last-game/<game_name>/<tag_line>', methods=['GET'])
def get_last_game(game_name, tag_line):
    return fetch_last_game(game_name, tag_line)

@match_bp.route('/parse-match/<game_name>/<tag_line>', methods=['GET'])
def parse_match(game_name, tag_line):
    return parse_match_data(game_name, tag_line)