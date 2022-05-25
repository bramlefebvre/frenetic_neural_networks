import numpy
from math import exp
from step_2.data_structures import Dynamics


def initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time):
    rate_matrix = _map_graph_to_rate_matrix(exuberant_system.graph, driving_value, initial_activity_parameter_factor, travel_time)
    return Dynamics(rate_matrix, exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)

def _map_graph_to_rate_matrix(graph, driving_value, initial_activity_parameter_factor, travel_time):
    number_of_states = len(graph)
    rate_matrix = numpy.zeros((number_of_states, number_of_states))
    for row in range(number_of_states):
        for column in range(number_of_states):
            rate_matrix[row, column] = _map_element(graph[row, column], driving_value, initial_activity_parameter_factor, travel_time)
    return rate_matrix

def _map_element(graph_value, driving_value, initial_activity_parameter_factor, travel_time):
    rate_matrix_value = 0
    initial_activity_parameter_value = (4 / travel_time) * exp(-driving_value / 2) * initial_activity_parameter_factor
    match graph_value:
        case 0:
            rate_matrix_value = initial_activity_parameter_value * exp(-driving_value / 2)
        case 1:
            rate_matrix_value = initial_activity_parameter_value * exp(driving_value / 2)
    return rate_matrix_value



    