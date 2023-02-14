'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2023 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


from daos.generate_strong_tournament import generate_random_strong_tournament
import daos.base_dao as base_dao
from step_1.data_structures import TournamentAndPatterns
import numpy
import numpy.typing as npt

def generate_single_tournament_and_patterns(number_of_states, patterns: tuple[frozenset[int], ...], id = None):
    tournament: npt.NDArray[numpy.int_] = generate_random_strong_tournament(number_of_states)
    return TournamentAndPatterns(tournament, patterns, id)

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
        'id': tournament_and_patterns.id
    }
    base_dao.add_single_entry(serialized, filename)

def _deserialize_tournament_and_patterns(serialized):
    tournament = numpy.array(serialized['tournament'], dtype = int)
    patterns = to_tuple_of_sets(serialized['patterns'])
    id = serialized['id']
    return TournamentAndPatterns(tournament, patterns, id)

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