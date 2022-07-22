import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

def plot_a_success():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/algorithm_3/s50_p5_av_n200_high')

    sorted_results = {}
    for result in training_data_list:
        initial_activity_parameter_factor = result.initial_activity_parameter_factor
        if initial_activity_parameter_factor not in sorted_results:
            sorted_results[initial_activity_parameter_factor] = []
        sorted_results[initial_activity_parameter_factor].append(result)

    initial_activity_parameter_factor_list = []
    success_chance_list = []

    for initial_activity_parameter_factor, results in sorted_results.items():
        initial_activity_parameter_factor_list.append(initial_activity_parameter_factor)
        number = 0
        successes = 0
        for result in results:
            number += 1
            if result.success:
                successes += 1
        success_chance_list.append(successes / number)
    
    plt.scatter(initial_activity_parameter_factor_list, success_chance_list)
    plt.xlabel('initial activity parameter factor')
    plt.ylabel('success chance')
    plt.show()
