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


from step_2.calculate_path import calculate_path

def calculate_performance(dynamics, desired_residence_time, n):
    rate_matrix = dynamics.rate_matrix
    number_of_states = len(rate_matrix)
    number_of_successes = 0
    number_of_verifications = n * number_of_states
    for _ in range(n):
        for initial_state in range(number_of_states):
            path = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
            if path is None:
                continue
            final_state_of_path = path.path['state'][-1]
            basin_for_state = dynamics.get_basin_for_state(initial_state)
            if final_state_of_path in basin_for_state.pattern_vertices and desired_residence_time <= path.residence_time_last_state:
                number_of_successes += 1
    return number_of_successes / number_of_verifications