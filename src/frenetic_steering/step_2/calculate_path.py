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


import numpy
from frenetic_steering.step_2.data_structures import Path

random_number_generator = numpy.random.default_rng()

def calculate_path(rate_matrix, initial_state: int, travel_time):
    number_of_states = len(rate_matrix)
    path: list[tuple[float, int]] = [(0, initial_state)]
    jump_time = 0
    state = initial_state
    residence_time: float = 0
    while jump_time < travel_time:
        if _path_is_too_long(path, number_of_states):
            return
        rates_for_state = rate_matrix[state, :]
        escape_rate = rates_for_state.sum()
        residence_time = random_number_generator.exponential(1/escape_rate)
        jump_time += residence_time
        if jump_time < travel_time:
            state = _decide_where_to_jump_to(rates_for_state, escape_rate)
            path.append((jump_time, state))
    datatype = numpy.dtype([('jump_time', float), ('state', int)])
    finished_path = numpy.array(path, datatype)
    return Path(finished_path, residence_time)


def _path_is_too_long(path, number_of_states) -> bool:
    return len(path) > 100 * number_of_states


def _decide_where_to_jump_to(rates_for_state, escape_rate) -> int:
    if escape_rate == numpy.Inf:
        return numpy.cumsum(rates_for_state).tolist().index(numpy.Inf)
    probabilities = [rate_for_state / escape_rate for rate_for_state in rates_for_state]
    return random_number_generator.choice(len(probabilities), p = probabilities)