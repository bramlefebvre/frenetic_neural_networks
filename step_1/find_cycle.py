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


from dataclasses import dataclass
from typing import Iterable
import numpy
import numpy.typing as npt
from step_1.data_structures import BasinUnderConstruction
from step_1.find_disentangled_system import CycleFindingProgressForBasin

random_number_generator = numpy.random.default_rng()

def find_cycle(graph: npt.NDArray[numpy.int_], cycle_finding_progress_for_basin: CycleFindingProgressForBasin, basins: tuple[BasinUnderConstruction, ...]):
    available_vertices = _get_available_vertices(len(graph), cycle_finding_progress_for_basin, basins)
    if len(available_vertices) < cycle_finding_progress_for_basin.length_of_cycle_to_find:
        return FindCycleResponse(None, True)
    pattern_vertex = _pick_one(cycle_finding_progress_for_basin.pattern_vertices_not_in_a_cycle)
    path = pattern_vertex,
    cycle = _continue_path(path, graph, available_vertices, cycle_finding_progress_for_basin.length_of_cycle_to_find - 1)
    return FindCycleResponse(cycle)


@dataclass(frozen = True)
class FindCycleResponse:
    cycle: tuple[int, ...] | None
    did_not_have_enough_available_vertices: bool = False
    

def _continue_path(path: tuple[int, ...], graph: npt.NDArray[numpy.int_], available_vertices: frozenset[int], number_of_vertices_left: int) -> tuple[int, ...] | None:
    forward_vertices = _get_forward_vertices(path, graph, available_vertices)
    if number_of_vertices_left == 1:
        return _finish_path(path, graph, forward_vertices)
    else:
        for forward_vertex in forward_vertices:
            new_path_list = list(path)
            new_path_list.append(forward_vertex)
            new_path = tuple(new_path_list)
            cycle = _continue_path(new_path, graph, available_vertices, number_of_vertices_left - 1)
            if cycle is not None:
                return cycle
        return None



def _finish_path(path: tuple[int, ...], graph: npt.NDArray[numpy.int_], forward_vertices: list[int]) -> tuple[int, ...] | None:
    for forward_vertex in forward_vertices:
        if graph[forward_vertex, path[0]] == 1:
            new_path_list = list(path)
            new_path_list.append(forward_vertex)
            return tuple(new_path_list)
    


def _get_forward_vertices(path: tuple[int, ...], graph: npt.NDArray[numpy.int_], available_vertices: frozenset[int]):
    last_vertex_in_path = path[-1]
    graph_values = graph[last_vertex_in_path, :]
    forward_vertices = list(filter(lambda vertex: vertex not in set(path) and graph_values[vertex] == 1, available_vertices))
    random_number_generator.shuffle(forward_vertices)
    return forward_vertices
    

def _get_available_vertices(number_of_vertices: int, cycle_finding_progress_for_basin: CycleFindingProgressForBasin, basins: tuple[BasinUnderConstruction, ...]) -> frozenset[int]:
    all_vertices_in_a_basin = set()
    all_vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - all_vertices_in_a_basin | cycle_finding_progress_for_basin.basin.vertices


def _pick_one(states: Iterable[int]) -> int:
    return random_number_generator.choice(list(states))


