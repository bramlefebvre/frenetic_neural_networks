import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt


def filter_result(result):
    return result.training_set_size == 4 * result.number_of_states and round(result.initial_activity_parameter_factor, 2) == round(result.number_of_states / result.number_of_patterns * 4 / 10, 2) \
        and result.number_of_patterns == 2

def plot_s_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_3/sv_p1_a5_n4x_all_leaving')
    # filtered_training_results = list(filter(filter_result, training_results))

    sorted_results = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)

    number_of_states_list = []
    performance_list = []

    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
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
    plt.scatter(number_of_states_list, performance_list)
    plt.xlabel('number of states')
    plt.ylabel('performance')
    plt.show()