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


from enum import Enum, unique

from step_2.data_structures import Action


def apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate):
    for rate_change_instruction in rate_change_instructions:
        transition = rate_change_instruction.transition
        factor = _get_factor_rate_change(rate_change_instruction.action, learning_rate)
        rate_matrix[transition[0], transition[1]] += factor * rate_matrix[transition[0], transition[1]]
        rate_matrix[transition[1], transition[0]] += factor * rate_matrix[transition[1], transition[0]]

def _get_factor_rate_change(action, learning_rate):
    if action == Action.INCREASE:
        factor = 1 / learning_rate - 1
    else:
        assert action == Action.DECREASE
        factor = learning_rate - 1
    return factor

def determine_path_type(input, path_with_jump_times, residence_time_last_state, desired_residence_time):
    if _ever_left_pattern_state(input):
        path_type = PathType.EVER_LEFT_PATTERN_STATE
    else:
        if _last_state_is_a_pattern_state(input):
            residence_time_in_pattern = _residence_time_in_pattern(input, path_with_jump_times, residence_time_last_state)
            if desired_residence_time <= residence_time_in_pattern: 
                path_type = PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH
            else:
                path_type = PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON
        else:
            path_type = PathType.NEVER_VISITED_PATTERN_STATE
    return path_type

def _residence_time_in_pattern(input, path_with_jump_times, residence_time_last_state):
    index_first_pattern_state = _index_first_pattern_state(input)
    jump_time_first_pattern_state = path_with_jump_times[index_first_pattern_state]['jump_time']
    jump_time_last_state = path_with_jump_times[-1]['jump_time']
    return jump_time_last_state - jump_time_first_pattern_state + residence_time_last_state

def _index_first_pattern_state(input):
    path = input.path
    pattern_states = input.pattern_states
    for index, state in enumerate(path):
        if state in pattern_states:
            return index
    raise ValueError('no state in pattern_states found')

def _ever_left_pattern_state(input):
    path = input.path
    pattern_states = input.pattern_states
    index_last_state = len(path) - 1
    for index, state in enumerate(path):
        if index != index_last_state:
            if state in pattern_states and path[index + 1] not in pattern_states:
                return True
    return False

def _last_state_is_a_pattern_state(input):
    return input.path[-1] in input.pattern_states

class GetRateChangeInstructionsFunctionInput:
    def __init__(self, graph, path, pattern_states):
        self.graph = graph
        self.path = path
        self.pattern_states = pattern_states

@unique
class PathType(Enum):
    ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH = 1
    EVER_LEFT_PATTERN_STATE = 2
    NEVER_VISITED_PATTERN_STATE = 3
    ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON = 4