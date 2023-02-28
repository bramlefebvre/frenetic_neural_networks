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
import math
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_disentangled_system import find_disentangled_system

random_number_generator = numpy.random.default_rng()

def generate_single_state_patterns(number_of_states, number_of_patterns):
    if number_of_patterns > number_of_states:
        raise ValueError('Number of patterns bigger than number of states')
    states: list[int] = list(range(number_of_states))
    patterns = []
    for _ in range(number_of_patterns):
        state: int = _pick_one(states)
        patterns.append([state])
        states.remove(state)
    return to_tuple_of_sets(patterns)

def to_sizes_of_basins(exuberant_system) -> list[int]:
    basins = exuberant_system.basins
    sizes_of_basins: list[int] = []
    for basin in basins:
        size_of_basin = len(basin.vertices) - len(basin.pattern_vertices)
        sizes_of_basins.append(size_of_basin)
    return sizes_of_basins

def generate_number_of_patterns_list(number_of_states):
    maximum_number_of_patterns = math.floor(number_of_states / 4)
    step = 1
    if maximum_number_of_patterns > 200:
        step = math.floor(maximum_number_of_patterns / 100)
    return list(range(2, maximum_number_of_patterns + 1, step))

def generate_disentangled_systems(number_of_states, number_of_patterns):
    patterns = generate_single_state_patterns(number_of_states, number_of_patterns)
    disentangled_systems = []
    for i in range(10):
        tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
        disentangled_system = find_disentangled_system(tournament_and_patterns).disentangled_system
        id = {
            'number_of_states': number_of_states,
            'number_of_patterns': number_of_patterns,
            'index': i
        }
        disentangled_system.id = id
        disentangled_systems.append(disentangled_system)
    return disentangled_systems

def result_is_successful(result):
    return all(map(lambda size_of_basin: _basin_is_big_enough(size_of_basin, result), result.sizes_of_basins))

def _basin_is_big_enough(size_of_basin, result):
    return size_of_basin > 1 / result.number_of_patterns * math.log(result.number_of_states)

def _pick_one(states: Iterable[int]) -> int:
    return random_number_generator.choice(list(states))

def to_tuple_of_sets(iterable_of_iterables) -> tuple[frozenset[int], ...]:
    result: list[frozenset[int]] = []
    for iterable in iterable_of_iterables:
        result.append(frozenset(iterable))
    return tuple(result)

