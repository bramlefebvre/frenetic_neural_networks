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


from statistics import mean
from daos.step_1_training_analysis_data_dao import save_training_data
from step_1.data_structures import TrainingAnalysisData
from step_1.Moon_version.find_disentangled_system import find_disentangled_system
import timeit
import time
import analysis_util
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns

def get_mean(getter, results):
    data = list(map(getter, results))
    return mean(data)

def get_mean_duration(results):
    return get_mean(lambda x: x.calculation_duration, results)

low = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
high = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

number_of_states_list = [100]
number_of_patterns_list = [5]

def calculation_duration():
    for number_of_states in number_of_states_list:
        results = []
        number_of_patterns_list = analysis_util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            print('[number_of_states, number_of_patterns]:')
            print([number_of_states, number_of_patterns])
            for i in range(10):
                patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
                tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
                for j in range(10):
                    timer = timeit.Timer(lambda: find_disentangled_system(tournament_and_patterns, True), timer = time.process_time)
                    times_executed, total_duration = timer.autorange()
                    calculation_duration =  (total_duration / times_executed) * 10 ** 3
                    result = TrainingAnalysisData(number_of_states, number_of_patterns, None, calculation_duration)
                    results.append(result)
        save_training_data(results, 'data/step_1/eliminate_cycles/calc_s100_pv')



