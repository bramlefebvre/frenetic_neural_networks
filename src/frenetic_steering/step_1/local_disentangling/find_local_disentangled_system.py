from dataclasses import dataclass
from frenetic_steering.step_1.data_structures import DisentangledSystem, CompletedBasin
from frenetic_steering.step_1.local_disentangling.find_closest_pattern import find_closest_pattern
from frenetic_steering.step_1.local_disentangling.util import number_of_spins_with_different_value
import numpy
import copy 
import numpy.typing as npt


type State = npt.NDArray[numpy.int8]

random_number_generator = numpy.random.default_rng()


def find_local_disentangled_system():
    pattern, distance = find_closest_pattern()
    cycle = _find_cycle(pattern)
    start_length_hair = _minimum_length_hair(input, cycle, distance)
    hair = _find_hair(cycle, input, start_length_hair)
    return _to_local_disentangled_system(cycle, hair)


def _minimum_length_hair(input, cycle, distance):
    pattern = cycle.cycle[0]
    number_of_flipped_spins = 0
    for flipped_spin in cycle.flipped_spins:
        if input[flipped_spin] != pattern[flipped_spin]:
            number_of_flipped_spins += 1
    minimum_length_hair = 0
    if number_of_flipped_spins > 0:
        minimum_length_hair = distance - number_of_flipped_spins
    else:
        minimum_length_hair = distance + 1
    return minimum_length_hair

def _to_local_disentangled_system(cycle, hair):
    pass

def _find_hair(cycle, input, start_length_hair):
    return _find_hair_with_length(cycle, input, start_length_hair)


def _find_hair_with_length(cycle, input, hair_length):
    hair = []
    hair.append(input)
    state = input
    
    # assume this hair_length works
    for i in range(1, hair_length):
        spins_with_different_value = _spins_with_different_value_excluding_cycle_flipped_spins(cycle, state)
        spin_to_flip = random_number_generator.choice(list(spins_with_different_value))
        state = _flip_spin_of_state(state, spin_to_flip)
        hair.append(state)
    index_closest_cycle_state = _get_index_closest_state(hair[-1], cycle.cycle[1:3])
    return Hair(index_closest_cycle_state, hair)

def _get_index_closest_state(state_0, states):
    distances = []
    for state in states:
        distances.append(number_of_spins_with_different_value(state, state_0))
    minimum_distance = min(distances)
    index_minimum = distances.index(minimum_distance)
    return index_minimum


def _spins_with_different_value_excluding_cycle_flipped_spins(cycle, state):
    central_cycle_state = cycle.cycle[3]
    spins_with_different_value = _spins_with_different_value(state, central_cycle_state)
    spins_with_different_value.difference_update(cycle.flipped_spins)
    return spins_with_different_value

def _spins_with_different_value(state_1, state_2):
    spins_with_different_value = set()
    for i, state_1_i in enumerate(state_1):
        if state_1_i != state_2[i]:
            spins_with_different_value.add(i)
    return spins_with_different_value

def _find_cycle(pattern: npt.NDArray[numpy.int8]):
    number_of_spins = len(pattern)
    spins = set(range(number_of_spins))
    spin_to_flip_1 = random_number_generator.choice(number_of_spins)
    spins.remove(spin_to_flip_1)
    spin_to_flip_2 = random_number_generator.choice(list(spins))
    cycle = []
    cycle.append(pattern)
    state = _flip_spin_of_state(pattern, spin_to_flip_1)
    cycle.append(state)
    state = _flip_spin_of_state(pattern, spin_to_flip_2)
    cycle.append(state)
    state = _flip_spin_of_state(pattern, spin_to_flip_1)
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
        
@dataclass(frozen = True)
class Cycle:
    flipped_spins: tuple[int, int]
    cycle: list[State]

@dataclass(frozen = True)
class Hair:
    index_destination_state_on_cycle: int
    hair: list[State]

@dataclass(frozen = True)
class LocalDisentangledSystem:
    index_to_state_map: dict[int, State]
    disentangled_system: DisentangledSystem
