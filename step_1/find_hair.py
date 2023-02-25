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


import numpy
import numpy.typing as npt

from step_1.data_structures import BasinUnderConstruction, FindHairResponse
from step_1.find_disentangled_system import HairFindingProgressForBasin

random_number_generator = numpy.random.default_rng()


def find_hair(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, basins: tuple[BasinUnderConstruction, ...]) -> FindHairResponse:
    free_vertices: frozenset[int] = _get_free_vertices(len(graph), basins)
    if len(free_vertices) == 0:
        find_hair_response: FindHairResponse = FindHairResponse(None, None, False, True)
    else:
        hair_length: int = hair_finding_progress_for_basin.length_of_hair_to_find
        path: tuple[int, int] | None = _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length)
        if path is None:
            hair_length += 1
            path = _find_hair_of_certain_length(graph, hair_finding_progress_for_basin, free_vertices, hair_length)
            if path is None:
                find_hair_response = FindHairResponse(None, None)
            else:
                find_hair_response = FindHairResponse(path[0], path[1], True)
        else:
            find_hair_response = FindHairResponse(path[0], path[1])
    return find_hair_response


def _find_hair_of_certain_length(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices: frozenset[int], hair_length: int) -> tuple[int, int] | None:
    if hair_length == 1:
        path: tuple[int, int] | None = _find_hair_of_length_1(graph, hair_finding_progress_for_basin, free_vertices)
    else:
        path = _find_hair_of_length_longer_than_1(graph, hair_finding_progress_for_basin, free_vertices, hair_length)
    return path

def _find_hair_of_length_1(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices: frozenset[int]) -> tuple[int, int] | None:
    possibilities: list[tuple[int, int]] = [(first_vertex, end_vertex) for first_vertex in free_vertices for end_vertex in hair_finding_progress_for_basin.non_pattern_vertices_in_a_cycle if graph[first_vertex, end_vertex] == 1]
    if len(possibilities) == 0:
        return None
    else:
        return _pick_one_arc(possibilities)

def _find_hair_of_length_longer_than_1(graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices: frozenset[int], hair_length: int) -> tuple[int, int] | None:
    shuffled_free_vertices: list[int] = list(free_vertices)
    random_number_generator.shuffle(shuffled_free_vertices)
    for new_vertex in shuffled_free_vertices:
        hair_vertex: int | None = _get_fitting_hair_vertex(new_vertex, graph, hair_finding_progress_for_basin, hair_length)
        if hair_vertex is not None:
            return (new_vertex, hair_vertex)
    

def _get_fitting_hair_vertex(new_vertex: int, graph: npt.NDArray[numpy.int_], hair_finding_progress_for_basin: HairFindingProgressForBasin, hair_length: int) -> int | None:
    hair_vertices: list[int] = [vertex for vertex in hair_finding_progress_for_basin.hair_vertices if graph[new_vertex, vertex] == 1 and _length_already_present_hair_fits(hair_finding_progress_for_basin, hair_length, vertex)]
    if len(hair_vertices) == 0:
        return None
    else:
        return _pick_one(hair_vertices)
    
def _length_already_present_hair_fits(hair_finding_progress_for_basin: HairFindingProgressForBasin, hair_length: int, already_present_hair_vertex: int) -> bool:
    number_of_vertices_left_to_add: int = hair_length - 1
    number_of_vertices_on_hair_starting_from_already_present_hair_vertex: int = _number_of_vertices_on_hair_starting_from_already_present_hair_vertex(hair_finding_progress_for_basin, already_present_hair_vertex)
    return number_of_vertices_left_to_add == number_of_vertices_on_hair_starting_from_already_present_hair_vertex

def _number_of_vertices_on_hair_starting_from_already_present_hair_vertex(hair_finding_progress_for_basin: HairFindingProgressForBasin, already_present_hair_vertex: int) -> int:
    number: int = 1
    arcs: set[tuple[int, int]] = hair_finding_progress_for_basin.basin.arcs
    destination: int = _destination_arc_starting_from_vertex(arcs, already_present_hair_vertex)
    while destination in hair_finding_progress_for_basin.hair_vertices:
        number += 1
        destination = _destination_arc_starting_from_vertex(arcs, destination)
    assert destination in hair_finding_progress_for_basin.non_pattern_vertices_in_a_cycle
    return number
        

def _destination_arc_starting_from_vertex(arcs: set[tuple[int, int]], vertex: int) -> int:
    destinations_of_arcs_starting_from_vertex: list[int] = [arc[1] for arc in arcs if arc[0] == vertex]
    assert len(destinations_of_arcs_starting_from_vertex) == 1
    return destinations_of_arcs_starting_from_vertex[0]

def _get_free_vertices(number_of_vertices: int, basins: tuple[BasinUnderConstruction, ...]) -> frozenset[int]:
    vertices_in_a_basin: set[int] = set()
    vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - vertices_in_a_basin

def _pick_one_arc(arcs: list[tuple[int, int]]) -> tuple[int, int]:
    return random_number_generator.choice(arcs)

def _pick_one(vertices: list[int]) -> int:
    return random_number_generator.choice(vertices)
