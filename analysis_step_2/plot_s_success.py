import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def plot_s_success():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_3/sv_p1_a4x_n4x')

    sorted_results = {}
    for result in training_data_list:
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
            if result.success:
                successes += 1
        success_chance_list.append(successes / number)

    plt.scatter(number_of_states_list, success_chance_list)
    plt.xlabel('number of states')
    plt.ylabel('success chance')
    plt.show()
