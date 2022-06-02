import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.number_of_states == 30 and result.number_of_patterns == 2 and result.initial_activity_parameter_factor == 6

def plot_n_performance():
    training_results = step_2_training_analysis_data_dao.get_training_data('data/step_2/training_results_0')
    filtered_training_results = list(filter(filter_result, training_results))

    sorted_training_results = {}
    for training_result in filtered_training_results:
        training_set_size = training_result.training_set_size
        if training_set_size not in sorted_training_results:
            sorted_training_results[training_set_size] = []
        sorted_training_results[training_set_size].append(training_result)

    training_set_size_list = []
    performance_list = []

    for training_set_size, training_results in sorted_training_results.items():
        training_set_size_list.append(training_set_size)
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

    plt.scatter(training_set_size_list, performance_list)
    plt.xlabel('training set size')
    plt.ylabel('performance')
    plt.show()