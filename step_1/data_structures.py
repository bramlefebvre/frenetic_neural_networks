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
from typing import Any
import numpy
import numpy.typing as npt
            


@dataclass(frozen = True)
class TournamentAndPatterns:
    tournament: npt.NDArray[numpy.int_]
    patterns: tuple[frozenset[int], ...]
    id: Any = None

@dataclass(frozen = True)
class CompletedBasin:
    index: int
    pattern_vertices: frozenset[int]
    vertices: frozenset[int]
    arcs: frozenset[tuple[int, int]]

@dataclass(frozen = True)
class BasinUnderConstruction:
    index: int
    pattern_vertices: frozenset[int]
    vertices: set[int]
    arcs: set[tuple[int, int]]

@dataclass
class DisentangledSystem:
    tournament_and_patterns_id: Any
    graph: npt.NDArray[numpy.int_]
    basins: tuple[CompletedBasin, ...]
    id: Any = None


@dataclass(frozen = True)
class TrainingResult:
    disentangled_system: DisentangledSystem


@dataclass
class TrainingAnalysisData:
    number_of_states: int
    number_of_patterns: int
    sizes_of_basins: list[int] | None
    calculation_duration: float | None

