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
from typing import Any
import numpy
import numpy.typing as npt


class DistanceCalculator:
    
    def get_distance_to_pattern_vertex_function(self, pattern_vertex):
        pass


@dataclass(frozen = True)
class GraphAndPatterns:
    graph: npt.NDArray[numpy.int_]
    patterns: tuple[frozenset[int], ...]
    id: Any = None

@dataclass(frozen = True)
class BasinUnderConstruction:
    index: int
    pattern_vertices: frozenset[int]
    vertices: set[int]
    arcs: set[tuple[int, int]]

@dataclass(frozen = True)
class FindCycleResponse:
    cycle: tuple[int, ...] | None
    no_cycle_can_be_found: bool = False

@dataclass
class CycleFindingProgressForBasin:
    basin: BasinUnderConstruction
    pattern_vertices_not_in_a_cycle: set[int] = field(init = False)
    length_of_cycle_to_find: int = 3
    no_cycle_can_be_found: bool = False

    def __post_init__(self):
        self.pattern_vertices_not_in_a_cycle = set(self.basin.pattern_vertices)
    
    def finished(self) -> bool:
        return self.no_cycle_can_be_found or len(self.pattern_vertices_not_in_a_cycle) == 0


@dataclass(frozen = True)
class FindHairResponse:
    new_vertex: int | None
    destination_vertex: int | None
    length_of_hair: int | None
    increase_length_of_hair_to_find: bool = False
    no_free_vertices_anymore: bool = False

@dataclass
class HairFindingProgressForBasin:
    basin: BasinUnderConstruction
    non_pattern_vertices_in_a_cycle: frozenset[int] = field(init = False)
    length_of_hair_to_find: int = 1
    hair_start_vertices_for_length: dict[int, set[int]] = field(default_factory=dict)
    vertex_could_be_added: bool = True

    def __post_init__(self):
        self.non_pattern_vertices_in_a_cycle = frozenset(self.basin.vertices - self.basin.pattern_vertices)
    
    def add_hair_element(self, new_vertex :int, destination_vertex: int, length_of_hair: int):
        self._add_hair_start_vertex(new_vertex, length_of_hair)
        self.basin.vertices.add(new_vertex)
        self.basin.arcs.add((new_vertex, destination_vertex))

    def _add_hair_start_vertex(self, new_vertex: int, length_of_hair: int):
        if not length_of_hair in self.hair_start_vertices_for_length:
            self.hair_start_vertices_for_length[length_of_hair] = set()
        self.hair_start_vertices_for_length[length_of_hair].add(new_vertex)


@dataclass(frozen = True)
class CompletedBasin:
    index: int
    pattern_vertices: frozenset[int]
    vertices: frozenset[int]


@dataclass(frozen = True)
class DisentangledSystem:
    graph_and_patterns_id: Any
    graph: npt.NDArray[numpy.int_]
    basins: tuple[CompletedBasin, ...]
    id: Any = None


@dataclass(frozen = True)
class TrainingResult:
    disentangled_system: DisentangledSystem


@dataclass(frozen = True)
class TrainingAnalysisData:
    number_of_states: int
    number_of_patterns: int
    fraction_of_arcs_present: float
    sizes_of_basins: list[int] | None
    calculation_duration: float | None

