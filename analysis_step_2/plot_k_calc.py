import daos.step_2_training_results_dao as step_2_training_results_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.number_of_states == 100 and result.training_set_size == 400 and result.initial_activity_parameter_factor == result.number_of_states / result.number_of_patterns * 4 / 10

def plot_k_calc():
    results = step_2_training_results_dao.get_calculation_duration_results('data/step_2/calculation_duration_0')
    filtered_results = list(filter(filter_result, results))

    sorted_results = {}
    for training_result in filtered_results:
        number_of_patterns = training_result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(training_result)

    number_of_patterns_list = []
    calculation_duration_list = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_calculation_durations = 0
        for training_result in results:
            number += 1
            summed_calculation_durations += training_result.calculation_duration      
        if number > 0:
            calculation_duration_list.append(summed_calculation_durations/number)
        else:
            calculation_duration_list.append(-0.1)

    plt.scatter(number_of_patterns_list, calculation_duration_list)
    plt.xlabel('number of patterns')
    plt.ylabel('calculation duration (ms)')
    plt.show()
