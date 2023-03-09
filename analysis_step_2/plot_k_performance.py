'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.number_of_states == 100 and result.training_set_size == 400 and round(result.initial_activity_parameter_factor, 2) == round(result.number_of_states / result.number_of_patterns * 4 / 10, 2)

def plot_k_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/s1000_pv_a20_n4000')
    # filtered_training_results = list(filter(filter_result, training_data_list))

    sorted_results = {}
    for result in training_data_list:
        number_of_patterns = result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(result)

    number_of_patterns_list = []
    performance_list = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_performances = 0
        for result in results:
            if result.success:
                number += 1
                summed_performances += result.performance
        if number > 0:
            performance_list.append(summed_performances/number)
        else:
            performance_list.append(-0.1)


    plt.scatter(number_of_patterns_list, performance_list)
    plt.xlabel('number of patterns')
    plt.ylabel('performance')
    plt.show()