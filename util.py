import numpy
import math

random_number_generator = numpy.random.default_rng()

def generate_single_state_patterns(number_of_states, number_of_patterns):
    if number_of_patterns > number_of_states:
        raise ValueError('Number of patterns bigger than number of states')
    states = list(range(number_of_states))
    patterns = []
    for _ in range(number_of_patterns):
        state = _pick_one(states)
        patterns.append([state])
        states.remove(state)
    return patterns

def to_sizes_of_basins(exuberant_system):
    basins = exuberant_system.basins
    sizes_of_basins = []
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

def _pick_one(states):
    return list(states)[random_number_generator.integers(len(states))]

