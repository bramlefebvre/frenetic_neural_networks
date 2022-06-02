import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.number_of_states == 100 and result.training_set_size == 400 and result.initial_activity_parameter_factor == result.number_of_states / result.number_of_patterns * 4 / 10

def plot_k_success():
    training_results = step_2_training_analysis_data_dao.get_training_data('data/step_2/training_results_1')
    filtered_training_results = list(filter(filter_result, training_results))

    sorted_training_results = {}
    for training_result in filtered_training_results:
        number_of_patterns = training_result.number_of_patterns
        if number_of_patterns not in sorted_training_results:
            sorted_training_results[number_of_patterns] = []
        sorted_training_results[number_of_patterns].append(training_result)

    number_of_patterns_list = []
    success_chance_list = []

    for number_of_patterns, training_results in sorted_training_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        successes = 0
        for training_result in training_results:
            number += 1
            if training_result.success:
                successes += 1
        success_chance_list.append(successes / number)

    plt.scatter(number_of_patterns_list, success_chance_list)
    plt.xlabel('number of patterns')
    plt.ylabel('success chance')
    plt.show()