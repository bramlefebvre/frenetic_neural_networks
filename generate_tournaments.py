from generate_strong_tournament import generate_random_strong_tournament
import frenetic_neural_networks_io

simplest_pattern_description = 'two patterns, each with one state'

pattern_description_map = {
    'A': simplest_pattern_description, 
    'B': ''}

def generate_tournaments(number_of_states, number_to_generate, patterns, pattern_description_key, filename):
    new_tournaments = set()
    while len(new_tournaments) < number_to_generate:
        generated_tournament = generate_random_strong_tournament(number_of_states)
        new_tournaments.add(generated_tournament)
    existing_tournaments = frenetic_neural_networks_io.read_tournament_and_patterns_array(filename)
