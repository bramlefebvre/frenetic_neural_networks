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

# bad implementation: finds all cycles and then selects one of shortest length

from typing import Iterable
import numpy
import numpy.typing as npt
from frenetic_steering.step_1.data_structures import BasinUnderConstruction

random_number_generator = numpy.random.default_rng()


def find_cycle(graph: npt.NDArray[numpy.int_], basin: BasinUnderConstruction, basins: tuple[BasinUnderConstruction, ...]):
    available_vertices: frozenset[int] = _get_available_vertices(len(graph), basin, basins)
    assert len(basin.pattern_vertices) == 1
    pattern_vertex: int = list(basin.pattern_vertices)[0]
    path: list[int] = [pattern_vertex]
    cycles = _find_cycles(path, graph, available_vertices)
    if len(cycles) == 0:
        return None
    return _get_a_cycle_of_shortest_length(cycles)
    
def _get_a_cycle_of_shortest_length(cycles):
    cycles_for_length = {}
    for cycle in cycles:
        cycle_length = len(cycle)
        if cycle_length not in cycles_for_length:
            cycles_for_length[cycle_length] = []
        cycles_for_length[cycle_length].append(cycle)
    length_shortest_cycle = min(cycles_for_length.keys())
    return _pick_one_tuple(cycles_for_length[length_shortest_cycle])
        

def _find_cycles(path: list[int], graph: npt.NDArray[numpy.int_], available_vertices: frozenset[int]):
    forward_vertices: list[int] = _get_forward_vertices(path, graph, available_vertices)
    cycles = [_finish_cycle(path, vertex) for vertex in forward_vertices if graph[vertex, path[0]] == 1]
    if len(cycles) == 0:
        for forward_vertex in forward_vertices:
            new_path: list[int] = path.copy()
            new_path.append(forward_vertex)
            cycles.extend(_find_cycles(new_path, graph, available_vertices)) # gives memory error
    return cycles
    

def _finish_cycle(path, vertex):
    new_path_list: list[int] = path.copy()
    new_path_list.append(vertex)
    return tuple(new_path_list)


def _get_forward_vertices(path: list[int], graph: npt.NDArray[numpy.int_], available_vertices: frozenset[int]) -> list[int]:
    last_vertex_in_path: int = path[-1]
    forward_vertices: list[int] = [vertex for vertex in available_vertices if vertex not in path and graph[last_vertex_in_path, vertex] == 1]
    return forward_vertices

def _get_available_vertices(number_of_vertices: int, basin: BasinUnderConstruction, basins: tuple[BasinUnderConstruction, ...]) -> frozenset[int]:
    all_vertices_in_a_basin: set[int] = set()
    all_vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - all_vertices_in_a_basin | basin.vertices

def _pick_one_tuple(tuples: list[tuple[int, ...]]) -> tuple[int, ...]:
    index = random_number_generator.integers(len(tuples))
    return tuples[index]

def _pick_one(vertices: Iterable[int]) -> int:
    return random_number_generator.choice(list(vertices))


