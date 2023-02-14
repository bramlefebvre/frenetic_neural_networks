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
from step_1.data_structures import BasinUnderConstruction, CompletedBasin, TournamentAndPatterns
import numpy
import numpy.typing as npt

random_number_generator = numpy.random.default_rng()

def find_disentangled_system(tournament_and_patterns: TournamentAndPatterns):

    pass

class CycleFindingProgress:
    basin: BasinUnderConstruction
    length_of_cycle_to_find: int = 3
    pattern_vertices_in_cycle: set[int] = set()

    def __init__(self, basin: BasinUnderConstruction) -> None:
        self.basin = basin
    
    def all_pattern_vertices_in_cycle(self) -> bool:
        return self.basin.pattern_vertices.issubset(self.pattern_vertices_in_cycle)

def _find_basins(tournament_and_patterns: TournamentAndPatterns) -> tuple[CompletedBasin, ...]:
    basins: tuple[BasinUnderConstruction, ...] = _initialize_basins(tournament_and_patterns.patterns)
    free_vertices = _get_initial_free_vertices(tournament_and_patterns)
    tournament: npt.NDArray[numpy.int_] = tournament_and_patterns.tournament


def _find_cycles_containing_pattern_vertices(tournament: npt.NDArray[numpy.int_], basins: tuple[BasinUnderConstruction, ...]):
    progress: set[CycleFindingProgress] = set(map(lambda basin: CycleFindingProgress(basin), basins))
    while(len(progress) > 0):
        for cycleFindingProgress in progress:
            pass


def _find_cycle(tournament: npt.NDArray[numpy.int_], cycleFindingProgress: CycleFindingProgress, basins: tuple[BasinUnderConstruction, ...]):
    pattern_vertices_without_cycle = cycleFindingProgress.basin.pattern_vertices - cycleFindingProgress.pattern_vertices_in_cycle
    pattern_vertex = _pick_one(pattern_vertices_without_cycle)
    free_vertices = set(range(len(tournament))).difference_update(map(lambda x: x.vertices, basins))



def _pick_one(states: Iterable[int]) -> int:
    return random_number_generator.choice(list(states))

def _get_initial_free_vertices(tournament_and_patterns: TournamentAndPatterns):
    all_pattern_vertices = set()
    all_pattern_vertices.update(*tournament_and_patterns.patterns)
    return set(range(len(tournament_and_patterns.tournament))) - all_pattern_vertices

def _initialize_basins(patterns: tuple[frozenset[int], ...]) -> tuple[BasinUnderConstruction, ...]:
    basins: list[BasinUnderConstruction] = []
    for index, pattern_vertices in enumerate(patterns):
        basins.append(_initialize_basin(index, pattern_vertices))
    return tuple(basins)

def _initialize_basin(index: int, pattern_vertices: frozenset[int]) -> BasinUnderConstruction:
    return BasinUnderConstruction(index, pattern_vertices, set(pattern_vertices), set())




