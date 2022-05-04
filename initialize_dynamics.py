import numpy
from math import exp

e = 3
initial_activity_parameter_value = 0.5

def map_exuberant_system_to_dynamics(exuberant_system):
    rate_matrix = _map_tournament_to_rate_matrix(exuberant_system.tournament)
    basins = _map_basins(exuberant_system.basins)
    return Dynamics(rate_matrix, basins)

def _map_tournament_to_rate_matrix(tournament):
    number_of_states = len(tournament)
    rate_matrix = numpy.zeros((number_of_states, number_of_states))
    for row in range(number_of_states):
        for column in range(number_of_states):
            rate_matrix[row, column] = _map_element(tournament[row, column])
    return rate_matrix

def _map_element(exuberant_system_value):
    rate_matrix_value = 0
    if exuberant_system_value == 0:
        rate_matrix_value = initial_activity_parameter_value * exp(-e)
    else:
        assert exuberant_system_value == 1
        rate_matrix_value = initial_activity_parameter_value
    return rate_matrix_value

def _map_basins(exuberant_system_basins):
    return Basins(tuple(map(_map_basin, exuberant_system_basins)))

def _map_basin(exuberant_system_basin):
    return Basin(exuberant_system_basin.index, exuberant_system_basin.pattern_vertices, exuberant_system_basin.vertices)

class Dynamics:
    def __init__(self, rate_matrix, basins):
        self.rate_matrix = rate_matrix
        self.basins = basins

class Basins:
    def __init__(self, basins):
        self.basins = basins
    
    def get_basin_for_state(self, state):
        for basin in self.basins:
            if state in basin.states:
                return basin

class Basin:
    def __init__(self, index, pattern_states, states):
        self.index = index
        self.pattern_states = pattern_states
        self.states = states
    