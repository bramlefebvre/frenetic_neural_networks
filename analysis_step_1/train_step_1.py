from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.data_structures import TrainingResult
from step_1.find_exuberant_system import find_exuberant_system
from daos.step_1_training_results_dao import save_training_results
import util


def calculate_variance(sizes_of_basins):
    sum = 0
    for size_of_basin_0 in sizes_of_basins:
        for size_of_basin_1 in sizes_of_basins:
            sum += (size_of_basin_0 - size_of_basin_1) ** 2
    return (1 / (len(sizes_of_basins) ** 2)) * sum


def train():
    number_of_states_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for number_of_states in number_of_states_list:
        training_results = []
        number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            print('[number_of_states, number_of_patterns]:')
            print([number_of_states, number_of_patterns])
            for i in range(10):
                patterns = util.generate_single_state_patterns(number_of_states, number_of_patterns)
                tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
                for j in range(10):
                    exuberant_system = find_exuberant_system(tournament_and_patterns)
                    sizes_of_basins = util.to_sizes_of_basins(exuberant_system)
                    training_result = TrainingResult(number_of_states, number_of_patterns, sizes_of_basins)
                    training_results.append(training_result)
        save_training_results(training_results, 'data/step_1/training_results_0')
