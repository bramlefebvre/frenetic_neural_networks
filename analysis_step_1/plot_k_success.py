import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt
import analysis_util

def _filter_result(result):
    return result.number_of_states == 100

def plot_k_success():
    results = step_1_training_analysis_data_dao.get_training_data('data/step_1/training_data_1')
    filtered_results = list(filter(_filter_result, results))

    sorted_results = {}
    for result in filtered_results:
        number_of_patterns = result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(result)

    number_of_patterns_list = []
    success_chance_list = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        successes = 0
        for result in results:
            number += 1
            if analysis_util.result_is_successful(result):
                successes += 1
        success_chance_list.append(successes / number)
    
    plt.scatter(number_of_patterns_list, success_chance_list)
    plt.xlabel('number of patterns')
    plt.ylabel('success chance')
    plt.show()