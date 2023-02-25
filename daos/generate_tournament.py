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


import numpy
from step_1.Moon_version.find_hamilton_cycle import hamilton_cycle_complete_tournament_exists
import numpy.typing as npt

random_number_generator = numpy.random.default_rng()

def generate_strong_tournament(number_of_states):
    found: bool = False
    tournament = None
    while not found:
        tournament = generate_tournament(number_of_states)
        found = hamilton_cycle_complete_tournament_exists(tournament)
    assert tournament is not None
    return tournament

def generate_tournament(number_of_states):
    tournament = _generate_upper_half_random_tournament(number_of_states)
    _complete_tournament(tournament)
    return tournament

def _generate_upper_half_random_tournament(number_of_states) -> npt.NDArray[numpy.int_]:
    tournament: npt.NDArray[numpy.int_] = -numpy.ones((number_of_states, number_of_states), dtype = int)
    for row in range(number_of_states):
        for column in range(number_of_states):
            if column > row:
                tournament[row, column] = random_number_generator.integers(2)
    return tournament

def _complete_tournament(tournament):
    number_of_states = len(tournament)
    for row in range(number_of_states):
        for column in range(number_of_states):
            if row > column:
                tournament[row, column] = _reverse(tournament[column, row])

def _reverse(value):
    if value == 0:
        return 1
    else:
        assert value == 1
        return 0