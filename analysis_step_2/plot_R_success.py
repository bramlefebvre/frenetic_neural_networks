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

training_results = step_2_training_analysis_data_dao.get_training_data('step_2/algorithm_2/e10_a0.5_n40_Rv')


sorted_training_results = {}

learning_rates = [0.1 * i for i in range(1, 10)]

for learning_rate in learning_rates:
    sorted_training_results[learning_rate] = []

for training_result in training_results:
    sorted_training_results[training_result.learning_rate].append(training_result)

success_chance_array = []

for learning_rate in learning_rates:
    total = 0
    successes = 0
    for training_result in sorted_training_results[learning_rate]:
        total += 1
        if training_result.success:
            successes += 1
    success_chance_array.append(successes / total)

print(success_chance_array)

plt.scatter(learning_rates, success_chance_array)
plt.xlabel('learning rate')
plt.ylabel('success rate')
plt.show()