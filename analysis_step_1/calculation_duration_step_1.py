from statistics import mean
from daos.step_1_training_analysis_data_dao import save_training_data
from step_1.data_structures import TrainingAnalysisData
from step_1.find_exuberant_system import find_exuberant_system
import timeit
import time
import util
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns

def get_mean(getter, results):
    data = list(map(getter, results))
    return mean(data)

def get_mean_duration(results):
    return get_mean(lambda x: x.calculation_duration, results)

number_of_states_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

def calculation_duration():
    for number_of_states in number_of_states_list:
        results = []
        number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            print('[number_of_states, number_of_patterns]:')
            print([number_of_states, number_of_patterns])
            for i in range(10):
                patterns = util.generate_single_state_patterns(number_of_states, number_of_patterns)
                tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
                for j in range(10):
                    timer = timeit.Timer(lambda: find_exuberant_system(tournament_and_patterns), timer = time.process_time)
                    times_executed, total_duration = timer.autorange()
                    calculation_duration =  (total_duration / times_executed) * 10 ** 3
                    result = TrainingAnalysisData(number_of_states, number_of_patterns, None, calculation_duration)
                    results.append(result)
        save_training_data(results, 'data/step_1/calculation_duration_1')



