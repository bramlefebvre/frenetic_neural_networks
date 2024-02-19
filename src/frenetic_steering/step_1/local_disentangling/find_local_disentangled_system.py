from frenetic_steering.step_1.local_disentangling.find_closest_pattern import find_closest_pattern
import numpy
import copy 
import numpy.typing as npt

random_number_generator = numpy.random.default_rng()


def find_local_disentangled_system():
    pattern, distance = find_closest_pattern()
    cycle = _find_cycle(pattern)
    start_length_hair = _minimum_length_hair(input, cycle, distance)
    hair = _find_hair(cycle, input, start_length_hair)
    return _to_local_disentangled_system(cycle, hair)



def _find_cycle(pattern: npt.NDArray[numpy.int8]):
    number_of_spins = len(pattern)
    spins = set(range(number_of_spins))
    spin_to_flip_1 = random_number_generator.choice(number_of_spins)
    spins.remove(spin_to_flip_1)
    spin_to_flip_2 = random_number_generator.choice(list(spins))
    cycle = []
    cycle.append(pattern)
    state = _flip_spin_of_state(pattern, spin_to_flip_1)
    

    
def _flip_spin_of_state(state: npt.NDArray[numpy.int8], spin_to_flip):
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
        
