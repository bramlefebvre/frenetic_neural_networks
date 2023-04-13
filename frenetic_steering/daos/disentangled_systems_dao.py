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


import frenetic_steering.daos.base_dao as base_dao
import numpy
from frenetic_steering.step_1.data_structures import CompletedBasin, DisentangledSystem

def get_single_disentangled_system(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return deserialize_disentangled_system(serialized)

def get_disentangled_systems(filename):
    serialized_exuberant_systems = base_dao.read_data(filename)
    return list(map(deserialize_disentangled_system, serialized_exuberant_systems))

def save_disentangled_system(exuberant_system, filename):
    serialized = serialize_disentangled_system(exuberant_system)
    base_dao.add_single_entry(serialized, filename)

def generate_cycle(number_of_states):
    graph = -numpy.ones((number_of_states, number_of_states), dtype = int)
    basins = (CompletedBasin(0, frozenset({0}), frozenset(range(number_of_states))),)
    for vertex in range(number_of_states):
        if vertex == number_of_states - 1:
            graph[vertex, 0] = 1
            graph[0, vertex] = 0
        else:
            graph[vertex, vertex + 1] = 1
            graph[vertex + 1, vertex] = 0
    return DisentangledSystem(None, graph, basins)

def serialize_disentangled_system(exuberant_system):
    serialized = {
        'graph_and_patterns_id': exuberant_system.graph_and_patterns_id,
        'graph': exuberant_system.graph.tolist(),
        'basins': list(map(_serialize_basin, exuberant_system.basins)),
        'id': exuberant_system.id
    }
    return serialized 

def deserialize_disentangled_system(serialized):
    graph_and_patterns_id = serialized['graph_and_patterns_id']
    graph = numpy.array(serialized['graph'], dtype = int)
    basins = tuple(map(_deserialize_basin, serialized['basins']))
    id = serialized['id']
    return DisentangledSystem(graph_and_patterns_id, graph, basins, id)

def _deserialize_basin(serialized):
    pattern_vertices = frozenset(serialized['pattern_vertices'])
    vertices = frozenset(serialized['vertices'])
    return CompletedBasin(serialized['index'], pattern_vertices, vertices)

def _serialize_basin(basin):
    pattern_vertices = list(basin.pattern_vertices)
    pattern_vertices.sort()
    vertices = list(basin.vertices)
    vertices.sort()
    serialized = {
        'index': basin.index,
        'pattern_vertices': pattern_vertices,
        'vertices': vertices
    }
    return serialized