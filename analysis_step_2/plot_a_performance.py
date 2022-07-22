import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt


def _filter_result(result):
    return result.number_of_states == 20 and result.training_set_size == 20 and result.number_of_patterns == 2

def plot_a_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_2/c10_av_n40_normal')
    # filtered_training_results = list(_filter(filter_result, training_results))

    sorted_results = {}
    for result in training_data_list:
        initial_activity_parameter_factor = result.initial_activity_parameter_factor
        if initial_activity_parameter_factor not in sorted_results:
            sorted_results[initial_activity_parameter_factor] = []
        sorted_results[initial_activity_parameter_factor].append(result)

    initial_activity_parameter_factors = []
    performance_list = []
    for initial_activity_parameter_factor, results in sorted_results.items():
        initial_activity_parameter_factors.append(initial_activity_parameter_factor)
        number = 0
        summed_performances = 0
        for result in results:
            if result.success:
                number += 1
                summed_performances += result.performance
        if number > 0:
            performance_list.append(summed_performances/number)
        else:
            performance_list.append(-0.1)

    print(performance_list)

    plt.scatter(initial_activity_parameter_factors, performance_list)
    plt.xlabel('initial activity parameter factor')
    plt.ylabel('performance')
    plt.show()