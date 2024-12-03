import json
import os

class MatchDataParser:
  def __init__(self, file_path):
    """
    Initializes the parser with the JSON file path.

    Args: 
        file_path (str): Path the the match JSON file
    """
    self.file_path = file_path
    self.data = None

    self._load_file() # load json file on initialization

  
  def _load_file(self):
    """
    Loads JSON file and parses it into a dictionary
    Raises an exception if the file doesn't exist or is invalid
    """
    if not os.path.exists(self.file_path):
      raise FileNotFoundError(f"File not found: {self.file_path}")
    
    try: 
      with open(self.file_path, "r", encoding="utf-8") as file:
        self.data = json.load(file)
    except json.JSONDecodeError as e:
      raise ValueError(f"Invalid JSON file: {e}")
  
  def get_game_duration(self):
    """
    Retrieves the game duration from the match data
    """
    try: 
      return self.data["info"]["gameDuration"]
    except KeyError:
      raise ValueError("Game duration not found in match data.")
    
  def get_all_players(self):
    """
    Returns a list of all participants who participated in the match
    """
    match_participants = []
    try:
      for i in range(0,10): # there will always be 10 players in a game
        match_participants.append(f'{self.data["info"]["participants"][i]["riotIdGameName"]}')
        # f'Summoner {i+1}: {self.data["info"]["participants"][i]["riotIdGameName"]}'
      return match_participants
    # try: 
    #   return self.data["info"]["participants"][6]["riotIdGameName"]
    except KeyError:
      raise ValueError("Participants not found in match data")
    
    