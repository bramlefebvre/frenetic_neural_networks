import math
from statistics import mean
from daos.step_1_training_results_dao import save_calculation_duration_results
from step_1.data_structures import CalculationDurationResult, TrainingResultType
from step_1.find_exuberant_system import find_exuberant_system
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import timeit
import numpy
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns

random_number_generator = numpy.random.default_rng()

def generate_number_of_patterns_list(number_of_states):
    maximum_number_of_patterns = math.floor(number_of_states / 4)
    step = 1
    if maximum_number_of_patterns > 200:
        step = math.floor(maximum_number_of_patterns / 100)
    return list(range(2, maximum_number_of_patterns, step))

def generate_single_state_patterns(number_of_states, number_of_patterns):
    if number_of_patterns > number_of_states:
        raise ValueError('Number of patterns bigger than number of states')
    states = list(range(number_of_states))
    patterns = []
    for _ in range(number_of_patterns):
        state = _pick_one(states)
        patterns.append([state])
        states.remove(state)
    return patterns

def _pick_one(states):
    return list(states)[random_number_generator.integers(len(states))]

def get_mean(getter, results):
    data = list(map(getter, results))
    return mean(data)

def get_mean_duration(results):
    return get_mean(lambda x: x.calculation_duration, results)

# number_of_states_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

number_of_states_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

for number_of_states in number_of_states_list:
    results = []
    number_of_patterns_list = generate_number_of_patterns_list(number_of_states)
    for number_of_patterns in number_of_patterns_list:
        print('[number_of_states, number_of_patterns]:')
        print([number_of_states, number_of_patterns])
        for i in range(10):
            patterns = generate_single_state_patterns(number_of_states, number_of_patterns)
            tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
            for j in range(10):
                timer = timeit.Timer(lambda: find_exuberant_system(tournament_and_patterns))
                times_executed, total_duration = timer.autorange()
                calculation_duration_in_milliseconds =  (total_duration / times_executed) * 10 ** 3
                result = CalculationDurationResult(number_of_states, number_of_patterns, calculation_duration_in_milliseconds)
                results.append(result)
    save_calculation_duration_results(results, 'data/step_1/calculation_duration_2')



