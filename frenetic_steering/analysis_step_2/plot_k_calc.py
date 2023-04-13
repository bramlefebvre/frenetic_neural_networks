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

def plot_k_calc():
    results = step_2_training_analysis_data_dao.get_training_data('data/step_2/old_1/algorithm_3/calculation_duration_0')
    filtered_results = list(filter(filter_result, results))

    sorted_results = {}
    for training_result in filtered_results:
        number_of_patterns = training_result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(training_result)

    number_of_patterns_list = []
    calculation_duration_list = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_calculation_durations = 0
        for training_result in results:
            number += 1
            summed_calculation_durations += training_result.calculation_duration      
        if number > 0:
            calculation_duration_list.append(summed_calculation_durations/number)
        else:
            calculation_duration_list.append(-0.1)

    plt.scatter(number_of_patterns_list, calculation_duration_list)
    plt.xlabel('number of patterns')
    plt.ylabel('calculation duration (ms)')
    plt.show()
