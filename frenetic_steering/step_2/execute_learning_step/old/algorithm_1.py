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


from operator import le
from step_2.calculate_path import calculate_path
from step_2.data_structures import FailureLearningStepResult, LearningStepResult

def execute_learning_step(dynamics, initial_state, learning_rate):
    rate_matrix = dynamics.rate_matrix.copy()
    path_with_jump_times = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
    if path_with_jump_times is None:
        return FailureLearningStepResult()
    path = path_with_jump_times['state'].tolist()
    basin = dynamics.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_vertices
    if not _is_desired_path(path, pattern_states):
        _change_rates_complete_path(path, pattern_states, rate_matrix, learning_rate)
    return LearningStepResult(rate_matrix, path)

def _change_rates_complete_path(path, pattern_states, rate_matrix, learning_rate):
    index_last_state = len(path) - 1
    for index, state in enumerate(path):
        if index != index_last_state:
            next_state = path[index + 1]
            factor = _get_factor_rate_change(state, pattern_states, learning_rate)
            rate_matrix[state, next_state] += factor * rate_matrix[state, next_state]
            rate_matrix[next_state, state] += factor * rate_matrix[next_state, state]

def _get_factor_rate_change(state, pattern_states, learning_rate):
    if state in pattern_states:
        return learning_rate - 1
    else:
        return 1 / learning_rate - 1

def _is_desired_path(path, pattern_states):
    pattern_state_indices = _indices_state_is_a_pattern_state(path, pattern_states)
    if len(pattern_state_indices) == 1 and pattern_state_indices[0] == len(path) - 1:
        return True
    else:
        return False



def _indices_state_is_a_pattern_state(path, pattern_states):
    indices = []
    for index, state in enumerate(path):
        if state in pattern_states:
            indices.append(index)
    return indices