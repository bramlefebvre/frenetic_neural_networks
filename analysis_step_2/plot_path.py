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


from daos.disentangled_systems_dao import get_single_disentangled_system
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.calculate_performance import calculate_performance
from step_2.calculate_path import calculate_path
import matplotlib.pyplot as plt

exuberant_system = get_single_disentangled_system('example_thesis', 'data/exuberant_systems')

initial_dynamics = initialize_dynamics(exuberant_system, 5, 0.3, 1)
training_result = train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 32)
trained_dynamics = training_result.dynamics
performance = calculate_performance(training_result.dynamics, 0.2, 100)
print(performance)
path = calculate_path(initial_dynamics.rate_matrix, 3, 1)
print(path.path)
jump_times = path.path['jump_time'].tolist()
jump_times.append(1)
states = path.path['state'].tolist()
states.append(states[-1])

plt.step(jump_times, states, where='post')
plt.xlabel('time(s)')
plt.ylabel('state')
plt.show()