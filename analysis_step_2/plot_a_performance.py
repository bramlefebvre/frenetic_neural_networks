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


def _filter_result(result):
    return result.number_of_states == 20 and result.training_set_size == 20 and result.number_of_patterns == 2

def plot_a_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_3_eliminate_cycles/s50_p5_av_n200')
    # filtered_training_results = list(filter(_filter_result, training_results))

    sorted_results = {}
    for result in training_data_list:
        initial_activity_parameter_factor = result.initial_activity_parameter_factor
        if initial_activity_parameter_factor not in sorted_results:
            sorted_results[initial_activity_parameter_factor] = []
        sorted_results[initial_activity_parameter_factor].append(result)

    initial_activity_parameter_factors = []
    performance_list = []
    for initial_activity_parameter_factor, results in sorted_results.items():
        initial_activity_parameter_factors.append(initial_activity_parameter_factor)
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

    plt.scatter(initial_activity_parameter_factors, performance_list)
    plt.xlabel('initial activity parameter factor')
    plt.ylabel('performance')
    plt.show()