from generate_strong_tournament import generate_random_strong_tournament
import frenetic_neural_networks_io

simplest_pattern_description = 'two patterns, each with one state'

pattern_description_map = {
    'A': simplest_pattern_description, 
    'B': ''}

def generate_tournaments(number_of_states, number_to_generate, patterns, pattern_description_key, filename):
    new_tournaments = set()
    while len(new_tournaments) < number_to_generate:
        # todo complete tournament data
        generated_tournament = generate_random_strong_tournament(number_of_states)
        new_tournaments.add(generated_tournament)
    existing_tournaments = frenetic_neural_networks_io.read_tournament_and_patterns_array(filename)
    stripped_existing_tournaments = _strip_ids(existing_tournaments)
    new_tournaments -= stripped_existing_tournaments
    _add_ids(new_tournaments)
    updated_tournaments = existing_tournaments + list(new_tournaments)
    frenetic_neural_networks_io.write_tournament_and_patterns_array(updated_tournaments, filename)

def _add_ids(iterable_of_maps):
    for map in iterable_of_maps:
        map['id'] = 'id'

def _strip_ids(iterable_of_maps_with_id_field):
    frozenset(map(_remove_id_field, iterable_of_maps_with_id_field))

def _remove_id_field(map_with_id_field):
    del map_with_id_field['id']


def to_tuple_of_sets(iterable_of_iterables):
    result = []
    for iterable in iterable_of_iterables:
        result.append(frozenset(iterable))
    return tuple(result)
