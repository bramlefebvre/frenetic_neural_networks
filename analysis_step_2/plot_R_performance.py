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


import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def plot_R_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/s50_p5_a2_n100_Rv')
    sorted_results = {}

    for result in training_data_list:
        learning_rate = result.learning_rate
        if learning_rate not in sorted_results:
            sorted_results[learning_rate] = []
        sorted_results[learning_rate].append(result)

    learning_rate_list = []
    performance_list = []

    for learning_rate, results in sorted_results.items():
        learning_rate_list.append(learning_rate)
        number = 0
        summed_performances = 0
        for result in results:
            if result.success:
                number += 1
                summed_performances += result.performance
            else:
                print('NO SUCCESS!!!!!')
        if number > 0:
            performance_list.append(summed_performances/number)
        else:
            performance_list.append(-0.1)

    plt.scatter(learning_rate_list, performance_list)
    plt.xlabel('learning rate')
    plt.ylabel('$p_{fren}$')
    plt.show()

    # learning_rates = [0.1 * i for i in range(1, 10)]

    # for learning_rate in learning_rates:
    #     sorted_results[learning_rate] = []

    # for training_result in training_data_list:
    #     sorted_results[training_result.learning_rate].append(training_result)

    # performance_array = []

    # for learning_rate in learning_rates:
    #     number = 0
    #     summed_performances = 0
    #     for training_result in sorted_results[learning_rate]:
    #         if training_result.success:
    #             number += 1
    #             summed_performances += training_result.performance
    #     performance_array.append(summed_performances/number)

    # print(performance_array)

    