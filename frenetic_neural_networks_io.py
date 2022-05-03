import json
import os

def read_tournament_and_patterns_array(filename):
    filepath = _to_path(filename)
    tournament_and_patterns_array = []
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as f:
            tournament_and_patterns_array = json.load(f)
    return tournament_and_patterns_array

def write_tournament_and_patterns_array(tournament_and_patterns_array, filename):
    filepath = _to_path(filename)
    with open(filepath, 'w') as f:
        json.dump(tournament_and_patterns_array, f)

def _to_path(filename):
    return 'data/' + filename

# tournament_and_patterns = {'tournament': example1.tournament, 'patterns': example1.patterns}
