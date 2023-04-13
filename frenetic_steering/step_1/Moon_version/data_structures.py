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
from frenetic_steering.step_1.data_structures import DisentangledSystem


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
    disentangled_system: DisentangledSystem
    cycle_finding_history: list[CycleFindingEvent]

@dataclass(frozen = True)
class CompletedBasin:
    index: int
    pattern_vertices: frozenset[int]
    vertices: frozenset[int]