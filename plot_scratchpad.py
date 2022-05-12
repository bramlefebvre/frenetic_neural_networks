import daos.training_results_dao as training_results_dao
import matplotlib.pyplot as plt

from step_2.data_structures import TrainingResultStatus

training_results = training_results_dao.get_training_results('algorithm_2/e10_n80_Rv')


sorted_training_results = {}

learning_rates = [0.1 * i for i in range(3, 10)]

for learning_rate in learning_rates:
    sorted_training_results[learning_rate] = []

for training_result in training_results:
    sorted_training_results[training_result.learning_rate].append(training_result)

performance_array = []

for learning_rate in learning_rates:
    number = 0
    summed_performances = 0
    for training_result in sorted_training_results[learning_rate]:    
        if training_result.status == TrainingResultStatus.SUCCESS:
            number += 1
            summed_performances += training_result.performance
    performance_array.append(summed_performances/number)

print(performance_array)

plt.scatter(learning_rates, performance_array)
plt.xlabel('learning rate')
plt.ylabel('performance')
plt.show()