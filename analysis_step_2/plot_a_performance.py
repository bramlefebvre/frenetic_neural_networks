import daos.step_2_training_results_dao as step_2_training_results_dao
import matplotlib.pyplot as plt


def plot_a_performance():
    training_results = step_2_training_results_dao.get_training_results('data/step_2/cycle_s10_e5_av_n30_R0.5')

    sorted_training_results = {}
    initial_activity_parameter_factors = []
    for training_result in training_results:
        initial_activity_parameter_factor = training_result.initial_activity_parameter_factor
        if initial_activity_parameter_factor not in sorted_training_results:
            initial_activity_parameter_factors.append(initial_activity_parameter_factor)
            sorted_training_results[initial_activity_parameter_factor] = []
        sorted_training_results[initial_activity_parameter_factor].append(training_result)

    initial_activity_parameter_factors.sort()
    performance_array = []

    for initial_activity_parameter_factor in initial_activity_parameter_factors:
        number = 0
        summed_performances = 0
        for training_result in sorted_training_results[initial_activity_parameter_factor]:
            if training_result.success:
                number += 1
                summed_performances += training_result.performance
        if number > 0:
            performance_array.append(summed_performances/number)
        else:
            performance_array.append(-0.1)

    print(performance_array)

    plt.scatter(initial_activity_parameter_factors, performance_array)
    plt.xlabel('initial activity parameter factor')
    plt.ylabel('performance')
    plt.show()