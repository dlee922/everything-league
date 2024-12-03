# Routes for managing player data
from flask import Blueprint, jsonify, request
from app.services.player_service import get_all_players, add_players, delete_player

player_bp = Blueprint('player', __name__)

@player_bp.route('/players', methods=['GET'])
def players():
    return get_all_players()

@player_bp.route('/add-players/<game_name>/<tag_line>', methods=['POST'])
def add(game_name, tag_line):
    return add_players(game_name, tag_line)

@player_bp.route('/delete-player/<player_name>', methods=['DELETE'])
def delete(player_name):
    return delete_player(player_name)