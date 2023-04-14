
import frenetic_steering.daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt
import math

def plot_e_performance():
    training_data_list = step_2_training_analysis_data_dao.get_training_data('data/step_2/s50_p10_a20_n200_ev')
    # filtered_training_results = list(filter(_filter_result, training_results))

    sorted_results = {}
    for result in training_data_list:
        driving_value = result.driving_value
        if driving_value not in sorted_results:
            sorted_results[driving_value] = []
        sorted_results[driving_value].append(result)

    driving_value_list = []
    performance_list = []

    for driving_value, results in sorted_results.items():
        driving_value_list.append(driving_value)
        number = 0
        summed_performances = 0
        for result in results:
            if result.success:
                number += 1
                summed_performances += result.performance
            else:
                print('NO SUCCESS!!!!!')
        if number > 0:
            performance_list.append(summed_performances/number)
        else:
            performance_list.append(-0.1)

    # fig, ax = plt.subplots()
    
    # ax.set_xscale('log', base=math.e)
    # ax.scatter(driving_value_list, performance_list)
    
    # plt.show()

    print(driving_value_list)
    print(performance_list)

    # plt.scatter(driving_value_list, performance_list)
    # my_xticks = ['log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)', 'log(10)']
    # plt.xticks(driving_value_list, my_xticks)

    # plt.xlabel('driving value')
    # plt.ylabel('performance')
    # plt.show()
    
