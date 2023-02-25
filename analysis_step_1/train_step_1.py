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


from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.data_structures import TrainingAnalysisData
from step_1.find_disentangled_system import find_disentangled_system
from daos.step_1_training_analysis_data_dao import save_training_data
import analysis_util




low = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
high = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

def train():
    number_of_states_list = [1000]
    # number_of_patterns_list = [5]
    for number_of_states in number_of_states_list:
        training_data_list = []
        number_of_patterns_list = range(1, 501)
        for number_of_patterns in number_of_patterns_list:
            print('[number_of_states, number_of_patterns]:')
            print([number_of_states, number_of_patterns])
            for i in range(100):
                patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
                tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
                disentangled_system = find_disentangled_system(tournament_and_patterns).disentangled_system
                sizes_of_basins = analysis_util.to_sizes_of_basins(disentangled_system)
                training_data = TrainingAnalysisData(number_of_states, number_of_patterns, sizes_of_basins, None)
                training_data_list.append(training_data)
        save_training_data(training_data_list, 'data/step_1/s1000_pv')



        # for j in range(10):
        #             disentangled_system = find_disentangled_system(tournament_and_patterns).disentangled_system
        #             sizes_of_basins = analysis_util.to_sizes_of_basins(disentangled_system)
        #             training_data = TrainingAnalysisData(number_of_states, number_of_patterns, sizes_of_basins, None)
        #             training_data_list.append(training_data)
