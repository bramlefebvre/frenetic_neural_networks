import daos.step_1_training_results_dao as step_1_training_results_dao
from step_1.data_structures import TrainingResultType
import matplotlib.pyplot as plt

def get_sorted_training_results_of_type_configuration(filename):
    all_training_results = step_1_training_results_dao.get_training_results(filename)
    training_results = list(filter(lambda x: x.type == TrainingResultType.CONFIGURATION, all_training_results))
    sorted_training_results = {}
    for training_result in training_results:
        if training_result.number_of_states not in sorted_training_results:
            sorted_training_results[training_result.number_of_states] = {}
        for_number_of_states = sorted_training_results[training_result.number_of_states]
        for_number_of_states[training_result.number_of_patterns] = training_result
    return sorted_training_results

filename = 'data/step_1/training_results_test'

training_results = get_sorted_training_results_of_type_configuration(filename)


percentages = []
values = []
for number_of_states, for_number_of_states in training_results.items():
    for number_of_patterns, training_result in for_number_of_states.items():
        percentages.append(number_of_patterns / number_of_states)
        values.append(training_result.variance_of_sizes_of_basins)

plt.scatter(percentages, values)
plt.xlabel('percentage')
plt.ylabel('values')
plt.show()