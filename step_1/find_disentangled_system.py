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

from dataclasses import dataclass, field
from typing import Iterable
from step_1.data_structures import BasinUnderConstruction, CompletedBasin, TournamentAndPatterns
import numpy
import numpy.typing as npt
from enum import Enum, unique
from step_1.find_cycle import FindCycleResponse, find_cycle

random_number_generator = numpy.random.default_rng()

def find_disentangled_system(graph_and_patterns: TournamentAndPatterns):

    pass

@dataclass
class CycleFindingProgressForBasin:
    basin: BasinUnderConstruction
    pattern_vertices_not_in_a_cycle: set[int] = field(init = False)
    length_of_cycle_to_find: int = 3
    did_not_have_enough_available_vertices: bool = False

    def __post_init__(self):
        self.pattern_vertices_not_in_a_cycle = set(self.basin.pattern_vertices)
    
    def finished(self) -> bool:
        return self.did_not_have_enough_available_vertices or len(self.pattern_vertices_not_in_a_cycle) == 0

@dataclass
class HairFindingProgressForBasin:
    basin: BasinUnderConstruction
    non_pattern_vertices_in_a_cycle: frozenset[int] = field(init = False)
    length_of_hair_to_find: int = 1
    hair_vertices: set[int] = set()
    no_vertex_could_be_added: bool = False

    def __post_init__(self):
        self.non_pattern_vertices_in_a_cycle = frozenset(self.basin.vertices - self.basin.pattern_vertices)
    
    def add_hair_vertices(self, path: tuple[int, ...]):
        pass
        

def _find_basins(graph_and_patterns: TournamentAndPatterns) -> tuple[CompletedBasin, ...]:
    basins: tuple[BasinUnderConstruction, ...] = _initialize_basins(graph_and_patterns.patterns)
    graph: npt.NDArray[numpy.int_] = graph_and_patterns.tournament
    _find_cycles_containing_pattern_vertices(graph, basins)



def _find_hairs(graph: npt.NDArray[numpy.int_], basins: tuple[BasinUnderConstruction, ...]):
    hair_finding_progress = list(map(lambda basin: HairFindingProgressForBasin(basin), basins))
    while len(hair_finding_progress) > 0:
        for hair_finding_progress_for_basin in hair_finding_progress:
            pass




def _find_cycles_containing_pattern_vertices(graph: npt.NDArray[numpy.int_], basins: tuple[BasinUnderConstruction, ...]):
    cycle_finding_progress: list[CycleFindingProgressForBasin] = list(map(lambda basin: CycleFindingProgressForBasin(basin), basins))
    while len(cycle_finding_progress) > 0:
        for cycle_finding_progress_for_basin in cycle_finding_progress:
            find_cycle_response = find_cycle(graph, cycle_finding_progress_for_basin, basins)
            _handle_find_cycle_response(find_cycle_response, cycle_finding_progress_for_basin)
        cycle_finding_progress = list(filter(lambda x: not x.finished(), cycle_finding_progress))


def _handle_find_cycle_response(find_cycle_response: FindCycleResponse, cycle_finding_progress_for_basin: CycleFindingProgressForBasin):
    if find_cycle_response.cycle is None:
        if find_cycle_response.did_not_have_enough_available_vertices:
            cycle_finding_progress_for_basin.did_not_have_enough_available_vertices = True
        else:
            cycle_finding_progress_for_basin.length_of_cycle_to_find += 1
    else:
        cycle = find_cycle_response.cycle
        cycle_finding_progress_for_basin.pattern_vertices_not_in_a_cycle.difference_update(cycle)
        cycle_finding_progress_for_basin.basin.vertices.update(cycle)
        cycle_finding_progress_for_basin.basin.arcs.update(_cycle_to_arcs(cycle))
        cycle_finding_progress_for_basin.length_of_cycle_to_find += 1


def _cycle_to_arcs(cycle: tuple[int, ...]):
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
    return BasinUnderConstruction(index, pattern_vertices, set(), set(pattern_vertices), set())




