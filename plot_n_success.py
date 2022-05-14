import daos.training_results_dao as training_results_dao
import matplotlib.pyplot as plt

training_results = training_results_dao.get_training_results('algorithm_2/e5_a2_nv_R0.5_low')


sorted_training_results = {}

training_set_size_list = list(range(1, 21))

for training_set_size in training_set_size_list:
    sorted_training_results[training_set_size] = []

for training_result in training_results:
    sorted_training_results[training_result.training_set_size].append(training_result)

success_chance_array = []

for training_set_size in training_set_size_list:
    total = 0
    successes = 0
    for training_result in sorted_training_results[training_set_size]:
        total += 1
        if training_result.success:
            successes += 1
    success_chance_array.append(successes / total)

print(success_chance_array)

plt.scatter(training_set_size_list, success_chance_array)
plt.xlabel('training set size')
plt.ylabel('success rate')
plt.show()