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


from step_2.data_structures import Action, RateChangeInstruction
import numpy

random_number_generator = numpy.random.default_rng()

def get_rate_change_instructions(input):
    path = input.path
    graph = input.graph
    rate_change_instructions = set()
    for index, state in enumerate(path):
        graph_values_for_state = graph[state, :]
        rate_change_instructions_for_state = _get_rate_change_instructions_for_state(index, state, path, graph_values_for_state)
        rate_change_instructions.update(rate_change_instructions_for_state)
    return list(rate_change_instructions)

def _get_rate_change_instructions_for_state(index, state, path, graph_values_for_state):
    if index == len(path) - 1:
        rate_change_instructions = _increase_all_forward_arcs(state, graph_values_for_state)
    else:
        next_state_in_path = path[index + 1]
        if graph_values_for_state[next_state_in_path] == 1:
            rate_change_instructions = {RateChangeInstruction((state, next_state_in_path), Action.INCREASE)}
        else:
            rate_change_instructions = _increase_all_forward_arcs(state, graph_values_for_state)
    return rate_change_instructions

def _increase_all_forward_arcs(state, graph_values_for_state):
    rate_change_instructions = set()
    for other_state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            rate_change_instructions.add(RateChangeInstruction((state, other_state), Action.INCREASE))
    return rate_change_instructions


