import daos.training_results_dao as training_results_dao
import matplotlib.pyplot as plt

training_results = training_results_dao.get_training_results('step_2/algorithm_2/e5_a0.5_nv_R0.5_low')

sorted_training_results = {}

training_set_size_list = list(range(1, 21))

for training_set_size in training_set_size_list:
    sorted_training_results[training_set_size] = []

for training_result in training_results:
    sorted_training_results[training_result.training_set_size].append(training_result)

performance_array = []

for training_set_size in training_set_size_list:
    number = 0
    summed_performances = 0
    for training_result in sorted_training_results[training_set_size]:
        if training_result.success:
            number += 1
            summed_performances += training_result.performance
    if number > 0:
        performance_array.append(summed_performances/number)
    else:
        performance_array.append(-0.1)

print(performance_array)

plt.scatter(training_set_size_list, performance_array)
plt.xlabel('training set size')
plt.ylabel('performance')
plt.show()