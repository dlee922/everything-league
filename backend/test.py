from match_parser import MatchDataParser

file_path = "last_game_Hanskyeul_NA1.json"

try:
  # Initialize parser
  parser = MatchDataParser(file_path)
  game_duration = parser.get_game_duration()
  match_participants = parser.get_all_participants()
  print(f"Game duration: {game_duration}\n")
  print(f"Match Participants: {match_participants}\n")
except (FileNotFoundError, ValueError) as e:
  print(f"Error: {e}")
