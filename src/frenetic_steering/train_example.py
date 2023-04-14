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


from frenetic_steering.daos.graphs_and_patterns_dao import generate_single_tournament_and_patterns
from frenetic_steering.step_1.Moon_version.find_disentangled_system import find_disentangled_system
from frenetic_steering.step_2.calculate_path import calculate_path
from frenetic_steering.step_2.calculate_performance import calculate_performance
from frenetic_steering.step_2.data_structures import LearningAlgorithm
from frenetic_steering.step_2.initialize_dynamics import initialize_dynamics
from frenetic_steering.step_2.training import train_starting_with_random_vertex_n_times

def train_example():
    patterns = (frozenset({0}),)
    tournament_and_patterns = generate_single_tournament_and_patterns(100, patterns)
    exuberant_system = find_disentangled_system(tournament_and_patterns, False).disentangled_system
    # print('exuberant system found')
    # initial_dynamics = initialize_dynamics(exuberant_system, 5, 5, 1)
    # training_result = train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 400)
    # # print(calculate_path(training_result.dynamics.rate_matrix, 1, 1).path)
    # performance = calculate_performance(training_result.dynamics, 0.2, 100)
    # print(performance)

train_example()
