import numpy
from math import exp
from step_2.data_structures import Basin, Basins, Dynamics

e = 3
initial_activity_parameter_value = 2

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
    match exuberant_system_value:
        case 0:
            rate_matrix_value = initial_activity_parameter_value * exp(-e)
        case 1:
            rate_matrix_value = initial_activity_parameter_value
    return rate_matrix_value

def _map_basins(exuberant_system_basins):
    return Basins(tuple(map(_map_basin, exuberant_system_basins)))

def _map_basin(exuberant_system_basin):
    return Basin(exuberant_system_basin.index, exuberant_system_basin.pattern_vertices, exuberant_system_basin.vertices)


    