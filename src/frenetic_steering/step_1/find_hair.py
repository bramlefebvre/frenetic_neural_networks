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


from typing import Callable
import numpy
import numpy.typing as npt

from frenetic_steering.step_1.data_structures import BasinUnderConstruction, DistanceCalculator, FindHairResponse, HairFindingProgressForBasin

random_number_generator = numpy.random.default_rng()

def find_hair(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, basins: tuple[BasinUnderConstruction, ...], distance_calculator: DistanceCalculator | None = None) -> FindHairResponse:
    # only works for single state patterns
    pattern_vertex = next(iter(hair_finding_progress_for_basin.basin.pattern_vertices))
    distance_function: Callable[[int], float] | None
    if distance_calculator is None:
        distance_function = None
    else:
        distance_function = distance_calculator.get_distance_to_pattern_vertex_function(pattern_vertex)
    free_vertices: frozenset[int] = _get_free_vertices(len(graph), basins)
    if len(free_vertices) == 0:
        find_hair_response: FindHairResponse = FindHairResponse(None, None, None, False, True)
    else:
        hair_length: int = hair_finding_progress_for_basin.length_of_hair_to_find
        path: tuple[int, int] | None = _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length, distance_function)
        if path is None:
            if hair_length not in hair_finding_progress_for_basin.hair_start_vertices_for_length:
                return FindHairResponse(None, None, None)
            hair_length += 1
            path = _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length, distance_function)
            if path is None:
                find_hair_response = FindHairResponse(None, None, None)
            else:
                find_hair_response = FindHairResponse(path[0], path[1], hair_length, True)
        else:
            find_hair_response = FindHairResponse(path[0], path[1], hair_length)
    return find_hair_response


def _find_hair_of_certain_length(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices: frozenset[int], hair_length: int, distance_function: Callable[[int], float] | None = None) -> tuple[int, int] | None:
    if hair_length == 1:
        path: tuple[int, int] | None = _find_hair_of_length_1(graph, hair_finding_progress_for_basin, free_vertices, distance_function)
    else:
        path = _find_hair_of_length_longer_than_1(graph, hair_finding_progress_for_basin, free_vertices, hair_length, distance_function)
    return path

def _find_hair_of_length_1(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices: frozenset[int], distance_function: Callable[[int], float] | None = None) -> tuple[int, int] | None:
    possibilities: list[tuple[int, int]] = [(first_vertex, end_vertex) for first_vertex in free_vertices for end_vertex in hair_finding_progress_for_basin.non_pattern_vertices_in_a_cycle if graph[first_vertex, end_vertex] == 1]
    if len(possibilities) == 0:
        return None
    else:
        return _pick_one_arc(possibilities, distance_function)

def _find_hair_of_length_longer_than_1(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices: frozenset[int], hair_length: int, distance_function: Callable[[int], float] | None = None) -> tuple[int, int] | None:
    shuffled_free_vertices: list[int] = list(free_vertices)
    random_number_generator.shuffle(shuffled_free_vertices)
    if distance_function is not None:
        shuffled_free_vertices.sort(key=distance_function)
    for new_vertex in shuffled_free_vertices:
        hair_vertex: int | None = _get_fitting_hair_vertex(new_vertex, graph, hair_finding_progress_for_basin, hair_length)
        if hair_vertex is not None:
            return (new_vertex, hair_vertex)
    

def _get_fitting_hair_vertex(new_vertex: int, graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, hair_length: int) -> int | None:
    length_already_existing_hair: int = hair_length - 1
    assert length_already_existing_hair in hair_finding_progress_for_basin.hair_start_vertices_for_length
    fitting_start_vertices_existing_hair: set[int] = hair_finding_progress_for_basin.hair_start_vertices_for_length[length_already_existing_hair]
    hair_vertices: list[int] = [vertex for vertex in fitting_start_vertices_existing_hair if graph[new_vertex, vertex] == 1]

    if len(hair_vertices) == 0:
        return None
    else:
        return _pick_one(hair_vertices)


def _get_free_vertices(number_of_vertices: int, basins: tuple[BasinUnderConstruction, ...]) -> frozenset[int]:
    vertices_in_a_basin: set[int] = set()
    vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - vertices_in_a_basin

def _pick_one_arc(arcs: list[tuple[int, int]], distance_function: Callable[[int], float] | None = None) -> tuple[int, int]:
    if distance_function is None:
        response = tuple([vertex.item() for vertex in random_number_generator.choice(arcs)]) # type: ignore
    else:
        minimum_distance = min([distance_function(arc[0]) for arc in arcs])
        arcs_with_minimum_distance = [arc for arc in arcs if distance_function(arc[0]) == minimum_distance]
        response = tuple([vertex.item() for vertex in random_number_generator.choice(arcs_with_minimum_distance)]) # type: ignore
    return response # type: ignore

def _pick_one(vertices: list[int]) -> int:
    return random_number_generator.choice(vertices).item()
