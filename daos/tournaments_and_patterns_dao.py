from daos.generate_strong_tournament import generate_random_strong_tournament
import daos.base_dao as base_dao
from step_1.data_structures import PatternDescription, TournamentAndPatterns
import numpy

def generate_single_tournament_and_patterns(number_of_states, patterns: tuple[frozenset[int]], pattern_description = None, id = None):
    tournament = generate_random_strong_tournament(number_of_states)
    # patterns = to_tuple_of_sets(patterns)
    return TournamentAndPatterns(tournament, patterns, pattern_description, id)

def get_single_tournament_and_patterns(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return _deserialize_tournament_and_patterns(serialized)

def get_tournaments_and_patterns(filename):
    serialized_tournaments_and_patterns = base_dao.read_data(filename)
    return list(map(_deserialize_tournament_and_patterns, serialized_tournaments_and_patterns))

def save_single_tournament_and_patterns(tournament_and_patterns, filename):
    serialized = {
        'tournament': tournament_and_patterns.tournament.tolist(),
        'patterns': _to_list_of_ordered_lists(tournament_and_patterns.patterns),
        'pattern_description_id': tournament_and_patterns.pattern_description.id,
        'id': tournament_and_patterns.id
    }
    base_dao.add_single_entry(serialized, filename)

def _deserialize_tournament_and_patterns(serialized):
    tournament = numpy.array(serialized['tournament'], dtype = int)
    patterns = to_tuple_of_sets(serialized['patterns'])
    pattern_description_id = serialized['pattern_description_id']
    pattern_description = PatternDescription.from_id(pattern_description_id)
    id = serialized['id']
    return TournamentAndPatterns(tournament, patterns, pattern_description, id)

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