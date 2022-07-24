import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def _filter_result(result):
    return result.number_of_states == 20 and result.number_of_patterns == 2 and result.initial_activity_parameter_factor == 4

def plot_n_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_3/s50_p5_a4_nv')
    # filtered_training_results = list(filter(_filter_result, training_results))

    sorted_results = {}
    for result in training_data_list:
        training_set_size = result.training_set_size
        if training_set_size not in sorted_results:
            sorted_results[training_set_size] = []
        sorted_results[training_set_size].append(result)

    training_set_size_list = []
    performance_list = []

    for training_set_size, results in sorted_results.items():
        training_set_size_list.append(training_set_size)
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

    plt.scatter(training_set_size_list, performance_list)
    plt.xlabel('training set size')
    plt.ylabel('performance')
    plt.show()