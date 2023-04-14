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


import frenetic_steering.daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.number_of_states == 100 and result.training_set_size == 400 and round(result.initial_activity_parameter_factor, 2) == round(result.number_of_states / result.number_of_patterns * 4 / 10, 2)

# training_results = step_2_training_analysis_data_dao.get_training_data('data/step_2/old_1/algorithm_3/training_results_1')

def plot_k_success():
    training_results = step_2_training_analysis_data_dao.get_training_data('data/step_2/training_data_1')
    filtered_training_results = list(filter(filter_result, training_results))

    sorted_training_results = {}
    for training_result in filtered_training_results:
        number_of_patterns = training_result.number_of_patterns
        if number_of_patterns not in sorted_training_results:
            sorted_training_results[number_of_patterns] = []
        sorted_training_results[number_of_patterns].append(training_result)

    number_of_patterns_list = []
    success_chance_list = []

    for number_of_patterns, training_results in sorted_training_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        successes = 0
        for training_result in training_results:
            number += 1
            if training_result.success:
                successes += 1
        success_chance_list.append(successes / number)

    print(number_of_patterns_list)
    plt.scatter(number_of_patterns_list, success_chance_list)
    plt.xlabel('number of patterns')
    plt.ylabel('success chance')
    plt.show()