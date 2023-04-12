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


import numpy
import numpy.typing as npt
from math import exp
from step_2.data_structures import Dynamics


def initialize_dynamics(disentangled_system, driving_value, initial_activity_parameter_factor, travel_time):
    rate_matrix = _map_graph_to_rate_matrix(disentangled_system.graph, driving_value, initial_activity_parameter_factor, travel_time)
    return Dynamics(rate_matrix, disentangled_system, driving_value, initial_activity_parameter_factor, travel_time)

def _map_graph_to_rate_matrix(graph, driving_value, initial_activity_parameter_factor, travel_time) -> npt.NDArray[numpy.double]:
    number_of_states: int = len(graph)
    rate_matrix: npt.NDArray[numpy.double] = numpy.zeros((number_of_states, number_of_states))
    for row in range(number_of_states):
        for column in range(number_of_states):
            rate_matrix[row, column] = _map_element(graph[row, column], driving_value, initial_activity_parameter_factor, travel_time)
    return rate_matrix

def _map_element(graph_value, driving_value, initial_activity_parameter_factor, travel_time) -> float:
    rate_matrix_value: float
    initial_activity_parameter_value: float = (1 / travel_time) * exp(-driving_value / 2) * initial_activity_parameter_factor
    match graph_value:
        case 0:
            rate_matrix_value = initial_activity_parameter_value * exp(-driving_value / 2)
        case 1:
            rate_matrix_value = initial_activity_parameter_value * exp(driving_value / 2)
        case -1:
            rate_matrix_value = 0
        case _:
            raise ValueError('graph value was different from 0, 1 and -1')
    return rate_matrix_value



    