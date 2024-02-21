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
from frenetic_steering.step_1.data_structures import DisentangledSystem, CompletedBasin
from frenetic_steering.step_1.local_disentangling.find_closest_pattern import find_closest_pattern
from frenetic_steering.application_on_images.load_images import load_input
from frenetic_steering.step_1.local_disentangling.util import number_of_spins_with_different_value
import numpy
import copy 
import numpy.typing as npt

from frenetic_steering.application_on_images.show_image import show_image

type State = npt.NDArray[numpy.int8]

random_number_generator = numpy.random.default_rng()


def find_local_disentangled_system():
    pattern, distance = find_closest_pattern()
    cycle = _find_cycle(pattern)
    input = load_input()
    hair = _find_hair(cycle, input, distance)
    return _to_local_disentangled_system(cycle, hair)

@dataclass(frozen = True)
class Cycle:
    flipped_spins: tuple[int, int]
    cycle: list[State]

@dataclass(frozen = True)
class Hair:
    index_destination_state_on_cycle: int
    hair: list[State]

def _to_local_disentangled_system(cycle: Cycle, hair: Hair):
    hair_length = len(hair.hair)
    index_to_state_map: dict[int, State] = {}
    for i, state in enumerate(hair.hair):
        index_to_state_map[i] = state
    for i in range(4):
        index_cycle_state = (hair.index_destination_state_on_cycle + i) % 4
        index_to_state_map[hair_length + i] = cycle.cycle[index_cycle_state]
    number_of_states = hair_length + 4
    graph = _initialize_graph(number_of_states)
    pattern_vertices = frozenset([-hair.index_destination_state_on_cycle % 4 + hair_length])
    completed_basin = CompletedBasin(0, pattern_vertices, frozenset(range(number_of_states)), tuple(range(hair_length, hair_length + 4)))
    disentangled_system = DisentangledSystem(None, graph, (completed_basin, ), None)
    return LocalDisentangledSystem(index_to_state_map, disentangled_system)

def _initialize_graph(number_of_states):
    graph = -numpy.ones((number_of_states, number_of_states), dtype=numpy.int8)
    for i in range(number_of_states - 1):
        graph[i, i + 1] = 1
        graph[i + 1, i] = 0
    graph[number_of_states - 1, number_of_states - 4] = 1
    graph[number_of_states - 4, number_of_states - 1] = 0
    return graph

def _number_of_flipped_spins(cycle, input):
    pattern = cycle.cycle[0]
    number_of_flipped_spins = 0
    for flipped_spin in cycle.flipped_spins:
        if input[flipped_spin] != pattern[flipped_spin]:
            number_of_flipped_spins += 1
    return number_of_flipped_spins

def _find_hair(cycle, input, distance):
    number_of_flipped_spins = _number_of_flipped_spins(cycle, input)
    return _find_hair_with_minimal_length(cycle, input, number_of_flipped_spins, distance)


def _find_hair_with_minimal_length(cycle, input, number_of_flipped_spins, distance):
    # assume this hair_length works
    hair = []
    hair.append(input)
    state = input
    remaining_hair_length: int
    if number_of_flipped_spins == 0:
        spin_to_flip = random_number_generator.choice(cycle.flipped_spins)
        state = _flip_spin_of_state(state, spin_to_flip)
        hair.append(state)
        remaining_hair_length = distance
    else:
        remaining_hair_length = distance - number_of_flipped_spins
    
    for i in range(remaining_hair_length - 1):
        spins_with_different_value = _spins_with_different_value_excluding_cycle_flipped_spins(cycle, state)
        spin_to_flip = random_number_generator.choice(list(spins_with_different_value))
        state = _flip_spin_of_state(state, spin_to_flip)
        hair.append(state)
    index_closest_cycle_state = _get_index_closest_state(hair[-1], cycle.cycle[1:3]) + 1
    return Hair(index_closest_cycle_state, hair)

def _get_index_closest_state(state_0, states):
    distances = []
    for state in states:
        distances.append(number_of_spins_with_different_value(state, state_0))
    minimum_distance = min(distances)
    index_minimum = distances.index(minimum_distance)
    return index_minimum


def _spins_with_different_value_excluding_cycle_flipped_spins(cycle, state):
    central_cycle_state = cycle.cycle[2]
    spins_with_different_value = _spins_with_different_value(state, central_cycle_state)
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
    spin_to_flip_1: int = random_number_generator.choice(number_of_spins)
    spins.remove(spin_to_flip_1)
    spin_to_flip_2: int = random_number_generator.choice(list(spins))
    cycle = []
    cycle.append(pattern)
    state = _flip_spin_of_state(pattern, spin_to_flip_1)
    cycle.append(state)
    state = _flip_spin_of_state(state, spin_to_flip_2)
    cycle.append(state)
    state = _flip_spin_of_state(state, spin_to_flip_1)
    cycle.append(state)
    return Cycle((spin_to_flip_1, spin_to_flip_2), cycle)

    
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
        
def _initialize_index_to_state_function():
    pass

@dataclass(frozen = True)
class LocalDisentangledSystem:
    index_to_state_map: dict[int, State]
    disentangled_system: DisentangledSystem
