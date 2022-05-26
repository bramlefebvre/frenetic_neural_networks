import math
from statistics import mean
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_single_state_patterns
from step_1.data_structures import TrainingResult, TrainingResultType
from step_1.find_exuberant_system import find_exuberant_system
from daos.step_1_training_results_dao import save_training_results
import numpy

random_number_generator = numpy.random.default_rng()


def generate_number_of_states_list_exponential(start_values, length_factor):
    values = []
    for i in range(length_factor):
        values_to_add = [x * 10 ** i for x in start_values]
        values += values_to_add
    return values

def generate_number_of_patterns_list(number_of_states):
    maximum_number_of_patterns = math.floor(number_of_states / 4)
    step = 1
    if maximum_number_of_patterns > 1000:
        step = math.floor(maximum_number_of_patterns / 100)
    return list(range(2, maximum_number_of_patterns, step))

def to_sizes_of_basins(exuberant_system):
    basins = exuberant_system.basins
    sizes_of_basins = []
    for basin in basins:
        size_of_basin = len(basin.vertices) - len(basin.pattern_vertices)
        sizes_of_basins.append(size_of_basin)
    return sizes_of_basins

def calculate_variance(sizes_of_basins):
    sum = 0
    for size_of_basin_0 in sizes_of_basins:
        for size_of_basin_1 in sizes_of_basins:
            sum += (size_of_basin_0 - size_of_basin_1) ** 2
    return (1 / (len(sizes_of_basins) ** 2)) * sum

def calculate_variance_of_sizes_of_basins(exuberant_system):
    sizes_of_basins = to_sizes_of_basins(exuberant_system)
    return calculate_variance(sizes_of_basins)

def get_mean_variance_of_sizes_of_basins(training_results):
    variances_of_sizes_of_basins = list(map(lambda x: x.variance_of_sizes_of_basins, training_results))
    return mean(variances_of_sizes_of_basins)

def generate_single_state_patterns_0(number_of_patterns):
    patterns = []
    for pattern_index in range(number_of_patterns):
        patterns.append([pattern_index])
    return patterns

def generate_single_state_patterns(number_of_states, number_of_patterns):
    
    states = list(range(number_of_states))
    patterns = []


def _pick_one(states):
    return list(states)[random_number_generator.integers(len(states))]


length_factor = 3
start_values = [10, 20, 50]

number_of_states_list = generate_number_of_states_list_exponential(start_values, length_factor)

all_training_results = []
config_training_results = []
for number_of_states in number_of_states_list:
    number_of_patterns_list = generate_number_of_patterns_list(number_of_states)
    initial_tournaments_and_patterns = [generate_single_tournament_and_single_state_patterns(number_of_states, 1) for _ in range(10)]
    for number_of_patterns in number_of_patterns_list:
        print('[number_of_states, number_of_patterns]:')
        print([number_of_states, number_of_patterns])
        tournament_training_results = []
        for i in range(10):
            tournament_and_patterns = initial_tournaments_and_patterns[i]
            tournament_and_patterns.patterns = generate_single_state_patterns(number_of_patterns)
            exuberant_system_training_results = []
            for j in range(10):
                exuberant_system = find_exuberant_system(tournament_and_patterns)
                variance_of_sizes_of_basins = calculate_variance_of_sizes_of_basins(exuberant_system)
                exuberant_system_training_result = TrainingResult(TrainingResultType.EXUBERANT_SYSTEM, number_of_states, number_of_patterns, variance_of_sizes_of_basins)
                exuberant_system_training_results.append(exuberant_system_training_result)
                all_training_results.append(exuberant_system_training_result)
            mean_variance_of_sizes_of_basins = get_mean_variance_of_sizes_of_basins(exuberant_system_training_results)
            tournament_training_result = TrainingResult(TrainingResultType.TOURNAMENT, number_of_states, number_of_patterns, mean_variance_of_sizes_of_basins)
            tournament_training_results.append(tournament_training_result)
            all_training_results.append(tournament_training_result)
        mean_variance_of_sizes_of_basins = get_mean_variance_of_sizes_of_basins(tournament_training_results)
        config_training_result = TrainingResult(TrainingResultType.CONFIGURATION, number_of_states, number_of_patterns, mean_variance_of_sizes_of_basins)
        config_training_results.append(config_training_result)
        all_training_results.append(config_training_result)
    
save_training_results(all_training_results, 'data/step_1/training_results_exp_0')
