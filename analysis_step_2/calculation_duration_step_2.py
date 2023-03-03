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


from statistics import mean
from daos.step_2_training_analysis_data_dao import save_training_data
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from analysis_step_2.data_structures import TrainingAnalysisData
import analysis_util
import timeit
import time
import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao

def generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns):
    fraction = 1 / 10 * number_of_states / number_of_patterns
    return [fraction * 4]

def _get_mean(getter, results):
    data = [getter(result) for result in results]
    return mean(data)

def _get_mean_duration(results):
    return _get_mean(lambda x: x.calculation_duration, results)


algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/calc_s1000_p10_a20_n4000'

def calculation_duration():
    number_of_states_list = [1000]
    for number_of_states in number_of_states_list:
        results = []
        # number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        number_of_patterns_list = [10]
        for number_of_patterns in number_of_patterns_list:
            disentangled_systems = analysis_util.generate_disentangled_systems(number_of_states, number_of_patterns)
            # initial_activity_parameter_factors = generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns)
            initial_activity_parameter_factor_list = [20]
            for initial_activity_parameter_factor in initial_activity_parameter_factor_list:
                training_set_size_list = [4000]
                for training_set_size in training_set_size_list:
                    print('[number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size]:')
                    print([number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size])
                    for disentangled_system in disentangled_systems:
                        initial_dynamics = initialize_dynamics(disentangled_system, driving_value, initial_activity_parameter_factor, travel_time)
                        timer = timeit.Timer(lambda: train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size), timer = time.process_time)
                        times_executed, total_duration = timer.autorange()
                        calculation_duration = (total_duration / times_executed) * 10 ** 3
                        result = TrainingAnalysisData(disentangled_system.id, None, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, None, calculation_duration)
                        results.append(result)
        save_training_data(results, filename)



def print_mean_duration():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/calc_s1000_p10_a20_n4000')
    print(_get_mean_duration(training_data_list))