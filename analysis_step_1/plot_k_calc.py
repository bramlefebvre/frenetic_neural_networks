import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt

def _filter_result(result):
    return result.number_of_states == 1000

def plot_k_calc():
    training_data_list = step_1_training_analysis_data_dao.get_training_data('data/step_1/calc_s1000_pv')
    # filtered_results = list(filter(_filter_result, results))

    sorted_results = {}
    for result in training_data_list:
        number_of_patterns = result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(result)

    number_of_patterns_list = []
    calculation_duration_list = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_calculation_durations = 0
        for result in results:
            number += 1
            summed_calculation_durations += result.calculation_duration      
        calculation_duration_list.append(summed_calculation_durations / number)

    plt.scatter(number_of_patterns_list, calculation_duration_list)
    plt.xlabel('number of patterns')
    plt.ylabel('calculation duration (ms)')
    plt.show()