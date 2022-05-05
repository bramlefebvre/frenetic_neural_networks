from generate_strong_tournament import generate_random_strong_tournament
import dao

simplest_pattern_description = 'two patterns, each with one state'

pattern_description_map = {
    'A': simplest_pattern_description, 
    'B': ''}

def generate_tournaments(number_of_states, number_to_generate, patterns, pattern_description_key, filename):
    new_tournaments = []
    while len(new_tournaments) < number_to_generate:
        generated_tournament = generate_random_strong_tournament(number_of_states)
        new_tournament = {
            'tournament': generated_tournament.tolist(), 
            'patterns': patterns,
            'pattern_description_key': pattern_description_key}
        dao.append_if_not_present(new_tournaments, new_tournament)
    dao.add_data_no_duplicates(new_tournaments, filename)

def to_tuple_of_sets(iterable_of_iterables):
    result = []
    for iterable in iterable_of_iterables:
        result.append(frozenset(iterable))
    return tuple(result)
