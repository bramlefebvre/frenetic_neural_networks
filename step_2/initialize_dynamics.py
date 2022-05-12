import numpy
from math import exp
from step_2.data_structures import Dynamics


def initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time):
    rate_matrix = _map_tournament_to_rate_matrix(exuberant_system.tournament, driving_value, initial_activity_parameter_factor, travel_time)
    return Dynamics(rate_matrix, exuberant_system, driving_value, travel_time)

def _map_tournament_to_rate_matrix(tournament, driving_value, initial_activity_parameter_factor, travel_time):
    number_of_states = len(tournament)
    rate_matrix = numpy.zeros((number_of_states, number_of_states))
    for row in range(number_of_states):
        for column in range(number_of_states):
            rate_matrix[row, column] = _map_element(tournament[row, column], driving_value, initial_activity_parameter_factor, travel_time)
    return rate_matrix

def _map_element(exuberant_system_value, driving_value, initial_activity_parameter_factor, travel_time):
    rate_matrix_value = 0
    initial_activity_parameter_value = (2 / travel_time) * exp(-driving_value/2) * initial_activity_parameter_factor
    match exuberant_system_value:
        case 0:
            rate_matrix_value = initial_activity_parameter_value * exp(-driving_value/2)
        case 1:
            rate_matrix_value = initial_activity_parameter_value * exp(driving_value/2)
    return rate_matrix_value



    