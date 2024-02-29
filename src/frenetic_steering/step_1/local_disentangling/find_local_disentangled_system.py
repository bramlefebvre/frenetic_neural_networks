'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2024 Bram Lefebvre

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
from typing import Callable
from frenetic_steering.step_1.data_structures import DisentangledSystem, CompletedBasin
from frenetic_steering.step_1.local_disentangling.find_closest_pattern import find_closest_pattern
import numpy
import copy
import numpy.typing as npt


type State = npt.NDArray[numpy.byte]

random_number_generator = numpy.random.default_rng()


def find_local_disentangled_system(input):
    pattern, distance = find_closest_pattern(input)
    cycle = _find_cycle(pattern)
    hair = _find_hair(cycle, input, pattern, distance)
    return _to_local_disentangled_system(cycle, hair)


@dataclass(frozen = True)
class Cycle:
    pattern_value_flipped_spin_0: numpy.byte
    pattern_value_flipped_spin_1: numpy.byte
    flipped_spins: tuple[int, int]


@dataclass(frozen = True)
class Hair:
    input: State
    spin_flips: list[int]
    

def _to_local_disentangled_system(cycle: Cycle, hair: Hair):
    hair_length = len(hair.spin_flips)
    number_of_states = hair_length + 4
    graph = _initialize_graph(number_of_states)
    index_first_state_on_cycle = _index_first_state_on_cycle(cycle, hair)
    index_to_state_function: Callable[[int], State] = _initialize_index_to_state_function(cycle, hair, index_first_state_on_cycle)
    pattern_vertices = frozenset([-index_first_state_on_cycle % 4 + hair_length])
    completed_basin = CompletedBasin(0, pattern_vertices, frozenset(range(number_of_states)), tuple(range(hair_length, hair_length + 4)))
    disentangled_system = DisentangledSystem(None, graph, (completed_basin, ), None)
    return LocalDisentangledSystem(index_to_state_function, disentangled_system)


def _initialize_graph(number_of_states):
    graph = -numpy.ones((number_of_states, number_of_states), dtype=numpy.byte)
    for i in range(number_of_states - 1):
        graph[i, i + 1] = 1
        graph[i + 1, i] = 0
    graph[number_of_states - 1, number_of_states - 4] = 1
    graph[number_of_states - 4, number_of_states - 1] = 0
    return graph

def _number_of_flipped_spins(cycle: Cycle, input):
    number_of_flipped_spins = 0
    if cycle.pattern_value_flipped_spin_0 != input[cycle.flipped_spins[0]]:
        number_of_flipped_spins += 1
    if cycle.pattern_value_flipped_spin_1 != input[cycle.flipped_spins[1]]:
        number_of_flipped_spins += 1
    return number_of_flipped_spins


def _find_hair(cycle, input, pattern, distance):
    return _find_hair_with_minimal_length(cycle, input, pattern, distance)


def _find_hair_with_minimal_length(cycle, input, pattern, distance):
    number_of_flipped_spins = _number_of_flipped_spins(cycle, input)
    # assume this hair_length works
    spin_flips: list[int] = []
    remaining_hair_length: int
    if number_of_flipped_spins == 0:
        spin_to_flip = random_number_generator.choice(cycle.flipped_spins)
        spin_flips.append(spin_to_flip)
        remaining_hair_length = distance
    else:
        remaining_hair_length = distance - number_of_flipped_spins
    spins_with_different_value = _spins_with_different_value_excluding_cycle_flipped_spins(cycle, input, pattern)
    for i in range(remaining_hair_length):
        spin_to_flip = random_number_generator.choice(list(spins_with_different_value))
        spins_with_different_value.remove(spin_to_flip)
        spin_flips.append(spin_to_flip)
    return Hair(input, spin_flips)

def _get_value_of_spin_for_first_state_on_cycle(hair: Hair, spin: int):
    number_of_flips = len([spin_flip for spin_flip in hair.spin_flips if spin_flip == spin]) % 2
    value_of_spin_for_input = hair.input[spin]
    value: int
    if number_of_flips == 1:
        value = _flip_spin_value(value_of_spin_for_input)
    else:
        value = value_of_spin_for_input
    return value

def _spins_with_different_value_excluding_cycle_flipped_spins(cycle, state, pattern):
    spins_with_different_value = _spins_with_different_value(state, pattern)
    spins_with_different_value.difference_update(cycle.flipped_spins)
    return spins_with_different_value

def _spins_with_different_value(state_0, state_1):
    spins_with_different_value = set()
    for i, state_0_i in enumerate(state_0):
        if state_0_i != state_1[i]:
            spins_with_different_value.add(i)
    return spins_with_different_value


def _find_cycle(pattern: State):
    number_of_spins = len(pattern)
    spins = set(range(number_of_spins))
    spin_to_flip_0: int = random_number_generator.choice(number_of_spins)
    spins.remove(spin_to_flip_0)
    spin_to_flip_1: int = random_number_generator.choice(list(spins))
    pattern_value_flipped_spin_0 = pattern[spin_to_flip_0]
    pattern_value_flipped_spin_1 = pattern[spin_to_flip_1]
    return Cycle(pattern_value_flipped_spin_0, pattern_value_flipped_spin_1, (spin_to_flip_0, spin_to_flip_1))

    
def _flip_spin_of_state(state: State, spin_to_flip):
    state = copy.copy(state)
    state[spin_to_flip] = _flip_spin_value(state[spin_to_flip])
    return state


def _flip_spin_value(spin_value):
    flipped_spin_value = 0
    if spin_value == 1:
        flipped_spin_value = 0
    else:
        flipped_spin_value = 1
    return flipped_spin_value
        

def _initialize_index_to_state_function(cycle: Cycle, hair: Hair, index_first_state_on_cycle: int):
    spin_flips: list[int] = []
    spin_flips.extend(hair.spin_flips)
    for i in range(3):
        index = (index_first_state_on_cycle + i) % 2
        spin_flips.append(cycle.flipped_spins[index])
    def index_to_state(index: int):
        if index == 0:
            return hair.input
        state = hair.input
        for i in range(index - 1):
            state = _flip_spin_of_state(state, spin_flips[i])
        return state
    return index_to_state

    
def _index_first_state_on_cycle(cycle: Cycle, hair: Hair):
    values_spin_to_flip_0_equal = cycle.pattern_value_flipped_spin_0 == _get_value_of_spin_for_first_state_on_cycle(hair, cycle.flipped_spins[0])
    values_spin_to_flip_1_equal = cycle.pattern_value_flipped_spin_1 == _get_value_of_spin_for_first_state_on_cycle(hair, cycle.flipped_spins[1])
    assert not (values_spin_to_flip_0_equal and values_spin_to_flip_1_equal)
    index_first_state_on_cycle: int
    if values_spin_to_flip_0_equal:
        index_first_state_on_cycle = 3
    elif values_spin_to_flip_1_equal:
        index_first_state_on_cycle = 1
    else:
        index_first_state_on_cycle = 2
    return index_first_state_on_cycle


@dataclass(frozen = True)
class LocalDisentangledSystem:
    index_to_state_function: Callable[[int], State]
    disentangled_system: DisentangledSystem
