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


from typing import Iterable
import numpy
import numpy.typing as npt
from step_1.data_structures import BasinUnderConstruction, FindCycleResponse, CycleFindingProgressForBasin

random_number_generator = numpy.random.default_rng()



def find_cycle(graph: npt.NDArray[numpy.int_], cycle_finding_progress_for_basin: CycleFindingProgressForBasin, basins: tuple[BasinUnderConstruction, ...]) -> FindCycleResponse:
    available_vertices: frozenset[int] = _get_available_vertices(len(graph), cycle_finding_progress_for_basin, basins)
    if len(available_vertices) < cycle_finding_progress_for_basin.length_of_cycle_to_find:
        return FindCycleResponse(None, True)
    pattern_vertex: int = _pick_one(cycle_finding_progress_for_basin.pattern_vertices_not_in_a_cycle)
    path: list[int] = [pattern_vertex]
    cycle: tuple[int, ...] | None = _continue_path(path, graph, available_vertices, cycle_finding_progress_for_basin.length_of_cycle_to_find - 1)
    return FindCycleResponse(cycle)


def _continue_path(path: list[int], graph: npt.NDArray[numpy.int_], available_vertices: frozenset[int], number_of_vertices_left: int) -> tuple[int, ...] | None:
    forward_vertices: list[int] = _get_forward_vertices(path, graph, available_vertices)
    if number_of_vertices_left == 1:
        return _finish_path(path, graph, forward_vertices)
    else:
        for forward_vertex in forward_vertices:
            new_path: list[int] = path.copy()
            new_path.append(forward_vertex)
            cycle: tuple[int, ...] | None = _continue_path(new_path, graph, available_vertices, number_of_vertices_left - 1)
            if cycle is not None:
                return cycle


def _finish_path(path: list[int], graph: npt.NDArray[numpy.int_], forward_vertices: list[int]) -> tuple[int, ...] | None:
    for forward_vertex in forward_vertices:
        if graph[forward_vertex, path[0]] == 1:
            new_path_list: list[int] = path.copy()
            new_path_list.append(forward_vertex)
            return tuple(new_path_list)
    

def _get_forward_vertices(path: list[int], graph: npt.NDArray[numpy.int_], available_vertices: frozenset[int]) -> list[int]:
    last_vertex_in_path: int = path[-1]
    forward_vertices = set([vertex for vertex in available_vertices if vertex not in path and graph[last_vertex_in_path, vertex] == 1])
    path_without_last_vertex = path[:-1]
    vertices_to_exclude = [vertex for vertex in available_vertices if any([graph[vertex_in_path_not_last, vertex] == 1 for vertex_in_path_not_last in path_without_last_vertex])]
    forward_vertices.difference_update(vertices_to_exclude)
    forward_vertices_list = list(forward_vertices)
    random_number_generator.shuffle(forward_vertices_list)
    return forward_vertices_list
    

def _get_available_vertices(number_of_vertices: int, cycle_finding_progress_for_basin: CycleFindingProgressForBasin, basins: tuple[BasinUnderConstruction, ...]) -> frozenset[int]:
    all_vertices_in_a_basin: set[int] = set()
    all_vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - all_vertices_in_a_basin | cycle_finding_progress_for_basin.basin.vertices


def _pick_one(vertices: Iterable[int]) -> int:
    return random_number_generator.choice(list(vertices))


