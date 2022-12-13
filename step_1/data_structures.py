'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022 Bram Lefebvre

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
from enum import Enum, unique


class TournamentAndPatterns:
    def __init__(self, tournament, patterns, pattern_description = None, id = None):
        self.tournament = tournament
        self.patterns = patterns
        self.pattern_description = pattern_description
        self.id = id

# An ExuberantSystem is a disentangled system
class ExuberantSystem:
    def __init__(self, tournament_and_patterns_id, graph, basins, id = None):
        self.tournament_and_patterns_id = tournament_and_patterns_id
        self.graph = graph
        self.basins = basins
        self.id = id

@dataclass
class BasinUnderConstruction:
    index: int
    pattern_vertices: frozenset[int]
    cycles: set[tuple[int, ...]]
    vertices_included_in_a_cycle: set[int]
    length_of_next_cycle: int

@dataclass(frozen = True)
class CycleFindingEvent:
    basin_snapshot: BasinUnderConstruction
    new_cycle: tuple[int, ...]


@dataclass(frozen = True)
class TrainingResult:
    exuberant_system: ExuberantSystem
    cycle_finding_history: list[CycleFindingEvent]


@dataclass(frozen = True)
class CompletedBasin:
    index: int
    pattern_vertices: frozenset[int]
    vertices: frozenset[int]

@dataclass
class TrainingAnalysisData:
    number_of_states: int
    number_of_patterns: int
    sizes_of_basins: list[int] | None
    calculation_duration: float | None

@unique
class PatternDescription(Enum):
    TWO_PATTERNS_EACH_WITH_ONE_STATE = 1, 'two patterns, each with one state'

    def __init__(self, id, display_value):
        self.id = id
        self.display_value = display_value

    @classmethod
    def from_id(cls, id):
        for element in list(cls):
            if element.id == id:
                return element