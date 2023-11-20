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
from frenetic_steering.step_1 import find_disentangled_system
import frenetic_steering.analysis_util as analysis_util
import cProfile

number_of_states = 100
number_of_patterns = 5


patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
cProfile.run('find_disentangled_system.find_disentangled_system(tournament_and_patterns)', 'data/step_1/profile_data')


