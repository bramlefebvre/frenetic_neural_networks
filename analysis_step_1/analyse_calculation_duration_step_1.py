import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
from step_1.data_structures import TrainingResultType
import matplotlib.pyplot as plt


filename = 'data/step_1/calculation_duration_1'

results = step_1_training_analysis_data_dao.get_calculation_duration_results(filename)

def plot_dependency_on_N(results):
    number_of_states_list = []
    values = []
    for number_of_states, for_number_of_states in results.items():
        for number_of_patterns, result in for_number_of_states.items():
            number_of_states_list.append(number_of_states)
            values.append(result.calculation_duration)
    plt.scatter(number_of_states_list, values)
    plt.xlabel('number of states')
    plt.ylabel('calculation duration (ms)')
    plt.show()

def plot_dependency_on_k(results, desired_number_of_states):
    number_of_patterns_list = []
    values = []
    for number_of_states, for_number_of_states in results.items():
        if number_of_states == desired_number_of_states:
            for number_of_patterns, result in for_number_of_states.items():
                number_of_patterns_list.append(number_of_patterns)
                values.append(result.calculation_duration)
    plt.scatter(number_of_patterns_list, values)
    plt.xlabel('number of patterns')
    plt.ylabel('calculation duration (ms)')
    plt.show()

def plot_dependency_on_N_for_k(results, desired_number_of_patterns):
    number_of_states_list = []
    values = []
    for number_of_states, for_number_of_states in results.items():
        for number_of_patterns, result in for_number_of_states.items():
            if number_of_patterns == desired_number_of_patterns:
                number_of_states_list.append(number_of_states)
                values.append(result.calculation_duration)
    plt.scatter(number_of_states_list, values)
    plt.xlabel('number of states')
    plt.ylabel('calculation duration (ms)')
    plt.show()

plot_dependency_on_N_for_k(results, 2)
