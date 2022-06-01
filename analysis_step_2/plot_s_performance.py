import daos.step_2_training_results_dao as step_2_training_results_dao
import matplotlib.pyplot as plt


def filter_result(result):
    return result.training_set_size == 4 * result.number_of_states and result.initial_activity_parameter_factor == result.number_of_states / result.number_of_patterns * 4 / 10 \
        and result.number_of_patterns == 2

def plot_s_performance():
    training_results = step_2_training_results_dao.get_training_results('data/step_2/training_results_1')
    filtered_training_results = list(filter(filter_result, training_results))

    sorted_training_results = {}
    for training_result in filtered_training_results:
        number_of_states = training_result.number_of_states
        if number_of_states not in sorted_training_results:
            sorted_training_results[number_of_states] = []
        sorted_training_results[number_of_states].append(training_result)

    number_of_states_list = []
    performance_list = []

    for number_of_states, training_results in sorted_training_results.items():
        number_of_states_list.append(number_of_states)
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
    plt.scatter(number_of_states_list, performance_list)
    plt.xlabel('number of states')
    plt.ylabel('performance')
    plt.show()