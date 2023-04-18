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

from frenetic_steering.step_1.data_structures import BasinUnderConstruction, CompletedBasin, CycleFindingProgressForBasin, DisentangledSystem, HairFindingProgressForBasin, GraphAndPatterns, TrainingResult
import numpy
import numpy.typing as npt
from frenetic_steering.step_1.find_cycle import FindCycleResponse, find_cycle
from frenetic_steering.step_1.find_hair import FindHairResponse, find_hair

random_number_generator = numpy.random.default_rng()

def find_disentangled_system(graph_and_patterns: GraphAndPatterns) -> TrainingResult:
    basins: tuple[BasinUnderConstruction, ...] = _find_basins(graph_and_patterns)
    graph: npt.NDArray[numpy.int_] = _to_disentangled_system_graph(basins, len(graph_and_patterns.graph))
    completed_basins: tuple[CompletedBasin, ...] = tuple(map(_to_completed_basin, basins))
    return TrainingResult(DisentangledSystem(graph_and_patterns.id, graph, completed_basins))

def _to_disentangled_system_graph(basins: tuple[BasinUnderConstruction, ...], number_of_vertices: int) -> npt.NDArray[numpy.int_]:
    graph: npt.NDArray[numpy.int_] = -numpy.ones((number_of_vertices, number_of_vertices), dtype=int)
    arcs: set[tuple[int, int]] = set()
    arcs.update(*map(lambda basin: basin.arcs, basins))
    for arc in arcs:
        graph[arc[0], arc[1]] = 1
        graph[arc[1], arc[0]] = 0
    return graph

def _to_completed_basin(basin: BasinUnderConstruction) -> CompletedBasin:
    return CompletedBasin(basin.index, basin.pattern_vertices, frozenset(basin.vertices))


def _find_basins(graph_and_patterns: GraphAndPatterns) -> tuple[BasinUnderConstruction, ...]:
    basins: tuple[BasinUnderConstruction, ...] = _initialize_basins(graph_and_patterns.patterns)
    graph: npt.NDArray[numpy.int_] = graph_and_patterns.graph
    _find_cycles_containing_pattern_vertices(graph, basins)
    _find_hairs(graph, basins)
    return basins

def _find_hairs(graph: npt.NDArray[numpy.int_], basins: tuple[BasinUnderConstruction, ...]) -> None:
    hair_finding_progress: list[HairFindingProgressForBasin] = [HairFindingProgressForBasin(basin) for basin in basins if _size_of_basin(basin) > 0]
    _find_hairs_for_smaller_basins(graph, hair_finding_progress, basins)
    
    while len(hair_finding_progress) > 0:
        for hair_finding_progress_for_basin in hair_finding_progress:
            find_hair_response: FindHairResponse = find_hair(graph, hair_finding_progress_for_basin, basins)
            if find_hair_response.no_free_vertices_anymore:
                return
            _handle_find_hair_response(find_hair_response, hair_finding_progress_for_basin)
        hair_finding_progress = [progress for progress in hair_finding_progress if progress.vertex_could_be_added]


def _find_hairs_for_smaller_basins(graph: npt.NDArray[numpy.int_], hair_finding_progress: list[HairFindingProgressForBasin], basins: tuple[BasinUnderConstruction, ...]):
    size_biggest_basin = max([_size_of_basin(hair_finding_progress_for_basin.basin) for hair_finding_progress_for_basin in hair_finding_progress])
    progress_smaller_basins = [hair_finding_progress_for_basin for hair_finding_progress_for_basin in hair_finding_progress if 
                               _size_of_basin(hair_finding_progress_for_basin.basin) < size_biggest_basin]
    while len(progress_smaller_basins) > 0:
        size_smallest_basins = min([_size_of_basin(hair_finding_progress_for_basin.basin) for hair_finding_progress_for_basin in progress_smaller_basins])
        progress_smallest_basins = [hair_finding_progress_for_basin for hair_finding_progress_for_basin in progress_smaller_basins if _size_of_basin(hair_finding_progress_for_basin.basin) == size_smallest_basins]
        for hair_finding_progress_for_basin in progress_smallest_basins:
            find_hair_response = find_hair(graph, hair_finding_progress_for_basin, basins)
            if find_hair_response.no_free_vertices_anymore:
                return
            _handle_find_hair_response(find_hair_response, hair_finding_progress_for_basin)
        progress_smaller_basins = [hair_finding_progress_for_basin for hair_finding_progress_for_basin in progress_smaller_basins if 
                                   hair_finding_progress_for_basin.vertex_could_be_added and _size_of_basin(hair_finding_progress_for_basin.basin) < size_biggest_basin]


def _size_of_basin(basin: BasinUnderConstruction):
    return len(basin.vertices) - len(basin.pattern_vertices)


def _handle_find_hair_response(find_hair_response: FindHairResponse, hair_finding_progress_for_basin: HairFindingProgressForBasin) -> None:
    if find_hair_response.new_vertex is None:
        hair_finding_progress_for_basin.vertex_could_be_added = False
    else:
        assert find_hair_response.destination_vertex is not None and find_hair_response.length_of_hair is not None
        if find_hair_response.increase_length_of_hair_to_find:
            hair_finding_progress_for_basin.length_of_hair_to_find += 1
        hair_finding_progress_for_basin.add_hair_element(find_hair_response.new_vertex, find_hair_response.destination_vertex, find_hair_response.length_of_hair)
        

def _find_cycles_containing_pattern_vertices(graph: npt.NDArray[numpy.int_], basins: tuple[BasinUnderConstruction, ...]):
    cycle_finding_progress: list[CycleFindingProgressForBasin] = list(map(lambda basin: CycleFindingProgressForBasin(basin), basins))
    while len(cycle_finding_progress) > 0:
        for cycle_finding_progress_for_basin in cycle_finding_progress:
            find_cycle_response: FindCycleResponse = find_cycle(graph, cycle_finding_progress_for_basin, basins)
            _handle_find_cycle_response(find_cycle_response, cycle_finding_progress_for_basin)
        cycle_finding_progress = [progress for progress in cycle_finding_progress if not progress.finished()]


def _handle_find_cycle_response(find_cycle_response: FindCycleResponse, cycle_finding_progress_for_basin: CycleFindingProgressForBasin):
    if find_cycle_response.cycle is None:
        if find_cycle_response.no_cycle_can_be_found:
            cycle_finding_progress_for_basin.no_cycle_can_be_found = True
        else:
            cycle_finding_progress_for_basin.length_of_cycle_to_find += 1
    else:
        cycle: tuple[int, ...] = find_cycle_response.cycle
        cycle_finding_progress_for_basin.pattern_vertices_not_in_a_cycle.difference_update(cycle)
        cycle_finding_progress_for_basin.basin.vertices.update(cycle)
        cycle_finding_progress_for_basin.basin.arcs.update(_cycle_to_arcs(cycle))


def _cycle_to_arcs(cycle: tuple[int, ...]) -> set[tuple[int, int]]:
    arcs: set[tuple[int, int]] = set()
    for index, vertex in enumerate(cycle):
        arcs.add((cycle[index - 1], vertex))
    return arcs

def _initialize_basins(patterns: tuple[frozenset[int], ...]) -> tuple[BasinUnderConstruction, ...]:
    basins: list[BasinUnderConstruction] = []
    for index, pattern_vertices in enumerate(patterns):
        basins.append(_initialize_basin(index, pattern_vertices))
    return tuple(basins)

def _initialize_basin(index: int, pattern_vertices: frozenset[int]) -> BasinUnderConstruction:
    return BasinUnderConstruction(index, pattern_vertices, set(pattern_vertices), set())




