import daos.step_2_training_results_dao as step_2_training_results_dao
import matplotlib.pyplot as plt


def plot_a_performance():
    training_results = step_2_training_results_dao.get_training_results('data/step_2/cycle_s10_e5_av_n20_R0.5')

    sorted_training_results = {}
    for training_result in training_results:
        initial_activity_parameter_factor = training_result.initial_activity_parameter_factor
        if initial_activity_parameter_factor not in sorted_training_results:
            sorted_training_results[initial_activity_parameter_factor] = []
        sorted_training_results[initial_activity_parameter_factor].append(training_result)

    initial_activity_parameter_factors = []
    performance_list = []
    for initial_activity_parameter_factor, training_results in sorted_training_results.items():
        initial_activity_parameter_factors.append(initial_activity_parameter_factor)
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

    plt.scatter(initial_activity_parameter_factors, performance_list)
    plt.xlabel('initial activity parameter factor')
    plt.ylabel('performance')
    plt.show()