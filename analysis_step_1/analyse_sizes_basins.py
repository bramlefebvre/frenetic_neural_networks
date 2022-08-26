import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt

def plot_dependency_on_s():
    filename = 'data/step_1/sv_p5_high'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    
    sorted_results = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)
    
    number_of_states_list = []
    average_variance_list = []

    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        number = 0
        summed_variances = 0
        for result in results:
            number += 1
            summed_variances += _calculate_variance(result.sizes_of_basins)
        average_variance_list.append(summed_variances / number)

    plt.scatter(number_of_states_list, average_variance_list)
    plt.xlabel('number of states')
    plt.ylabel('variance size basins')
    plt.show()

def plot_dependency_on_k():
    filename = 'data/step_1/s1000_pv'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    
    sorted_results = {}
    for result in training_data_list:
        number_of_patterns = result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(result)
    
    number_of_patterns_list = []
    average_variance_list = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_variances = 0
        for result in results:
            number += 1
            summed_variances += _calculate_variance(result.sizes_of_basins)
        average_variance_list.append(summed_variances / number)

    plt.scatter(number_of_patterns_list, average_variance_list)
    plt.xlabel('number of patterns')
    plt.ylabel('variance size basins')
    plt.show()


def _calculate_average_difference(sizes_of_basins):
    pass

def _calculate_variance(sizes_of_basins: list[int]):
    sum = 0
    for size_of_basin_0 in sizes_of_basins:
        for size_of_basin_1 in sizes_of_basins:
            sum += (size_of_basin_0 - size_of_basin_1) ** 2
    return (1 / (len(sizes_of_basins) ** 2)) * sum

