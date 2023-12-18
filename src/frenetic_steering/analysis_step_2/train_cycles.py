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


import math
from frenetic_steering.analysis_step_2.data_structures import TrainingAnalysisData
from frenetic_steering.daos.disentangled_systems_dao import generate_cycle
from frenetic_steering.daos.step_2_training_analysis_data_dao import save_training_data
from frenetic_steering.step_2.data_structures import LearningAlgorithm
from frenetic_steering.step_2.initialize_dynamics import initialize_dynamics
from frenetic_steering.step_2.training import train_starting_with_random_vertex_n_times
from frenetic_steering.step_2.calculate_performance import calculate_performance


algorithm_2 = LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES
algorithm_3 = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC

algorithm = algorithm_3
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/cv_a5_nx'

# (success, disentangled_system_id, number_of_states, number_of_patterns, driving_value, 
# initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, 
# training_set_size, performance):

def generate_initial_activity_parameter_factors_list(number_of_states):
    max_activity_parameter_factor = 10 * math.ceil(number_of_states / 4)
    step = 1
    if max_activity_parameter_factor > 200:
        step = math.floor(max_activity_parameter_factor / 100)
    return list(range(1, max_activity_parameter_factor + 1, step))

def generate_training_set_size_list(number_of_states):
    max_training_set_size = 10 * number_of_states
    step = 1
    if max_training_set_size > 200:
        step = math.floor(max_training_set_size / 100)
    return list(range(1, max_training_set_size, step))

def train_cycles():
    number_of_states_list = range(3, 21)
    for number_of_states in number_of_states_list:
        training_data_list = []
        cycle = generate_cycle(number_of_states)
        initial_activity_parameter_factors = [5]
        for initial_activity_parameter_factor in initial_activity_parameter_factors:
            initial_dynamics = initialize_dynamics(cycle, driving_value, initial_activity_parameter_factor, travel_time)
            training_set_size_list = [number_of_states]
            for training_set_size in training_set_size_list:
                print('[number_of_states, initial_activity_parameter_factor, training_set_size]:')
                print([number_of_states, initial_activity_parameter_factor, training_set_size])
                for i in range(100):
                    training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
                    if training_result.success:
                        performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
                    else: 
                        performance = None
                    training_data = TrainingAnalysisData(training_result.success, number_of_states, 1, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
                    training_data_list.append(training_data)
        save_training_data(training_data_list, filename)

def train_cycles_R():
    learning_rate_list = [0.5]
    number_of_states = 10
    initial_activity_parameter_factor = 4
    training_set_size = 20
    cycle = generate_cycle(number_of_states)
    initial_dynamics = initialize_dynamics(cycle, driving_value, initial_activity_parameter_factor, travel_time)
    training_data_list = []
    for learning_rate in learning_rate_list:
        print('learning_rate:')
        print(learning_rate)
        for i in range(100):
            training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
            if training_result.success:
                performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
            else:
                performance = None
            training_data = TrainingAnalysisData(training_result.success, number_of_states, 1, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
            training_data_list.append(training_data)
    save_training_data(training_data_list, filename)
