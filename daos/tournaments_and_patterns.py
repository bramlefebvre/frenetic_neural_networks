from daos.generate_strong_tournament import generate_random_strong_tournament
import daos.base_dao as base_dao
from step_1.data_structures import TournamentAndPatterns
import numpy

simplest_pattern_description = 'two patterns, each with one state'

pattern_description_map = {
    'A': simplest_pattern_description, 
    'B': ''}


def generate_single_tournament_and_patterns(number_of_states, patterns, pattern_description_key = 'A', id = None):
    if pattern_description_key not in pattern_description_map:
        raise ValueError
    tournament = generate_random_strong_tournament(number_of_states)
    patterns = to_tuple_of_sets(patterns)
    return TournamentAndPatterns(tournament, patterns, pattern_description_key, pattern_description_map[pattern_description_key], id)

def get_single_tournament_and_patterns(id, filename):
    serialized = base_dao.read_entry(id, filename)
    tournament = numpy.array(serialized['tournament'])
    patterns = to_tuple_of_sets(serialized['patterns'])
    pattern_description_key = serialized['pattern_description_key']
    if pattern_description_key not in pattern_description_map:
        raise ValueError
    return TournamentAndPatterns(tournament, patterns, pattern_description_key, pattern_description_map[pattern_description_key], id)

def save_single_tournament_and_patterns(tournament_and_patterns, filename):
    serialized = {
        'tournament': tournament_and_patterns.tournament.tolist(),
        'patterns': _to_list_of_ordered_lists(tournament_and_patterns.patterns),
        'pattern_description_key': tournament_and_patterns.pattern_description_key,
        'id': tournament_and_patterns.id
    }
    base_dao.add_single_entry_no_duplicates(serialized, filename)

def generate_tournaments_and_patterns_and_save(number_of_states, number_to_generate, patterns, pattern_description_key, filename):
    if pattern_description_key not in pattern_description_map:
        raise ValueError
    new_tournaments = []
    while len(new_tournaments) < number_to_generate:
        generated_tournament = generate_random_strong_tournament(number_of_states)
        new_tournament = {
            'tournament': generated_tournament.tolist(), 
            'patterns': patterns,
            'pattern_description_key': pattern_description_key}
        base_dao.append_if_not_present(new_tournaments, new_tournament)
    base_dao.add_data_no_duplicates(new_tournaments, filename)

def _to_list_of_ordered_lists(iterable_of_iterables):
    result = []
    for iterable in iterable_of_iterables:
        inner_list = list(iterable)
        inner_list.sort()
        result.append(inner_list)
    return result

def to_tuple_of_sets(iterable_of_iterables):
    result = []
    for iterable in iterable_of_iterables:
        result.append(frozenset(iterable))
    return tuple(result)