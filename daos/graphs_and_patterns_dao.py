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


from typing import Any
from daos.generate_graph import generate_graph, generate_tournament
import daos.base_dao as base_dao
from step_1.data_structures import GraphAndPatterns
import numpy
import numpy.typing as npt


def generate_single_graph_and_patterns(number_of_states: int, patterns:  tuple[frozenset[int], ...], fraction_of_arcs_present: float, id: Any = None):
    graph_and_patterns: GraphAndPatterns
    if fraction_of_arcs_present == 1:
        graph_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns, id)
    else:
        graph = generate_graph(number_of_states, fraction_of_arcs_present)
        graph_and_patterns = GraphAndPatterns(graph, patterns, id)
    return graph_and_patterns


def generate_single_tournament_and_patterns(number_of_states: int, patterns: tuple[frozenset[int], ...], id: Any = None):
    tournament: npt.NDArray[numpy.int_] = generate_tournament(number_of_states)
    return GraphAndPatterns(tournament, patterns, id)

def get_single_graph_and_patterns(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return _deserialize_graph_and_patterns(serialized)

def get_graphs_and_patterns(filename: str) -> list[GraphAndPatterns]:
    serialized_tournaments_and_patterns = base_dao.read_data(filename)
    return list(map(_deserialize_graph_and_patterns, serialized_tournaments_and_patterns))

def save_single_graph_and_patterns(graph_and_patterns: GraphAndPatterns, filename: str):
    serialized = {
        'graph': graph_and_patterns.graph.tolist(),
        'patterns': _to_list_of_ordered_lists(graph_and_patterns.patterns),
        'id': graph_and_patterns.id
    }
    base_dao.add_single_entry(serialized, filename)

def _deserialize_graph_and_patterns(serialized) -> GraphAndPatterns:
    graph: npt.NDArray[numpy.int_] = numpy.array(serialized['graph'], dtype = int)
    patterns: tuple[frozenset[int], ...] = to_tuple_of_sets(serialized['patterns'])
    id = serialized['id']
    return GraphAndPatterns(graph, patterns, id)

def _to_list_of_ordered_lists(iterable_of_iterables):
    result = []
    for iterable in iterable_of_iterables:
        inner_list = list(iterable)
        inner_list.sort()
        result.append(inner_list)
    return result

def to_tuple_of_sets(iterable_of_iterables) -> tuple[frozenset[int], ...]:
    result = []
    for iterable in iterable_of_iterables:
        result.append(frozenset(iterable))
    return tuple(result)