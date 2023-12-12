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


import frenetic_steering.daos.graphs_and_patterns_dao as graphs_and_patterns_dao
import frenetic_steering.step_1.find_disentangled_system as find_disentangled_system
import pandas
from frenetic_steering.step_2.calculate_path import calculate_path
from frenetic_steering.step_2.calculate_performance import calculate_performance
from frenetic_steering.step_2.data_structures import LearningAlgorithm
from frenetic_steering.step_2.initialize_dynamics import initialize_dynamics
import frenetic_steering.step_2.training as training

def pprint(object):
    print(pandas.DataFrame(object))

def demo_all():
    number_of_vertices = 12
    serialized_patterns = [[0], [2], [3]]
    patterns = graphs_and_patterns_dao.to_tuple_of_sets(serialized_patterns)
    tournament_and_patterns = graphs_and_patterns_dao.generate_single_tournament_and_patterns(number_of_vertices, patterns)
    exuberant_system = find_disentangled_system.find_disentangled_system(tournament_and_patterns, None).disentangled_system
    print('original tournament:')
    pprint(tournament_and_patterns.graph)
    print('basins:')
    print([set(basin.vertices) for basin in exuberant_system.basins])
    print('graph:')
    pprint(exuberant_system.graph)

    travel_time = 1
    driving_value = 5
    initial_activity_parameter_factor = 2
    learning_rate = 0.5
    training_set_size = 40
    desired_residence_time = 0.2

    algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC

    dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
    print('initial rate matrix:')
    pprint(dynamics.rate_matrix)

    training_result = training.train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
    if training_result.success == True:
        dynamics = training_result.dynamics
        initial_state = 5
        path = calculate_path(dynamics.rate_matrix, initial_state, travel_time)
        if path is None:
            print('unsuccessful path')
        else:
            print('path:')
            print(path.path)
            performance = calculate_performance(dynamics, desired_residence_time, 100)
            print('performance:')
            print(performance)
    else:
        print('training failed!')