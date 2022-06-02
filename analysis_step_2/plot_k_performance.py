import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.number_of_states == 60 and result.training_set_size == 240 and round(result.initial_activity_parameter_factor, 2) == round(result.number_of_states / result.number_of_patterns * 4 / 10, 2)

def plot_k_performance():
    training_results = step_2_training_analysis_data_dao.get_training_data('data/step_2/old_1/algorithm_3/training_results_1')
    filtered_training_results = list(filter(filter_result, training_results))

    sorted_training_results = {}
    for training_result in filtered_training_results:
        number_of_patterns = training_result.number_of_patterns
        if number_of_patterns not in sorted_training_results:
            sorted_training_results[number_of_patterns] = []
        sorted_training_results[number_of_patterns].append(training_result)

    number_of_patterns_list = []
    performance_list = []

    for number_of_patterns, training_results in sorted_training_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_performances = 0
        for training_result in training_results:
            if training_result.success:
                number += 1
                summed_performances += training_result.performance
        if number > 0:
            performance_list.append(summed_performances/number)
        else:
            performance_list.append(-0.1)

    print(performance_list)

    plt.scatter(number_of_patterns_list, performance_list)
    plt.xlabel('number of patterns')
    plt.ylabel('performance')
    plt.show()