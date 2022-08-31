import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def filter_result(result):
    return result.training_set_size == 4 * result.number_of_states and round(result.initial_activity_parameter_factor, 2) == round(result.number_of_states / result.number_of_patterns * 4 / 10, 2) \
        and result.number_of_patterns == 2

def plot_s_calc():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_3/calc_sv_p1_a5_n4x')
    # filtered_results = list(filter(filter_result, results))

    sorted_results = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)

    number_of_states_list = []
    calculation_duration_list = []

    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        number = 0
        summed_calculation_durations = 0
        for result in results:
            number += 1
            summed_calculation_durations += result.calculation_duration
        if number > 0:
            calculation_duration_list.append(summed_calculation_durations/number)
        else:
            calculation_duration_list.append(-0.1)
    plt.scatter(number_of_states_list, calculation_duration_list)
    plt.xlabel('number of states')
    plt.ylabel('calculation duration (ms)')
    plt.show()