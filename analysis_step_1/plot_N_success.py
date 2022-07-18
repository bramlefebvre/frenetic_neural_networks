import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt
import analysis_util

def _filter_result(result):
    return result.number_of_patterns == 2


def plot_N_success():
    results = step_1_training_analysis_data_dao.get_training_data('data/step_1/training_data_0')
    filtered_results = list(filter(_filter_result, results))

    sorted_results = {}
    for result in filtered_results:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)
    
    number_of_states_list = []
    success_chance_list = []

    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        number = 0
        successes = 0
        for result in results:
            number += 1
            if analysis_util.result_is_successful(result):
                successes += 1
        success_chance_list.append(successes / number)


    plt.scatter(number_of_states_list, success_chance_list)
    plt.xlabel('number of states')
    plt.ylabel('success chance')
    plt.show()
