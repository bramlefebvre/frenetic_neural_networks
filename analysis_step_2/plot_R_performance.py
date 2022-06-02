import daos.step_2_training_analysis_data_dao as step_2_training_analysis_data_dao
import matplotlib.pyplot as plt

training_results = step_2_training_analysis_data_dao.get_training_data('step_2/algorithm_2/e10_a0.5_n40_Rv')


sorted_training_results = {}

learning_rates = [0.1 * i for i in range(1, 10)]

for learning_rate in learning_rates:
    sorted_training_results[learning_rate] = []

for training_result in training_results:
    sorted_training_results[training_result.learning_rate].append(training_result)

performance_array = []

for learning_rate in learning_rates:
    number = 0
    summed_performances = 0
    for training_result in sorted_training_results[learning_rate]:
        if training_result.success:
            number += 1
            summed_performances += training_result.performance
    performance_array.append(summed_performances/number)

print(performance_array)

plt.scatter(learning_rates, performance_array)
plt.xlabel('learning rate')
plt.ylabel('performance')
plt.show()