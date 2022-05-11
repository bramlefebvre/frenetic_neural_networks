import daos.training_results_dao as training_results_dao
from step_2.data_structures import TrainingResultStatus
import matplotlib.pyplot as plt
import numpy as np

training_results = training_results_dao.get_training_results('training_results_R')


sorted_training_results = {}

learning_rates = [0.1 * i for i in range(1, 10)]

for learning_rate in learning_rates:
    sorted_training_results[learning_rate] = []

for training_result in training_results:
    sorted_training_results[training_result.learning_rate].append(training_result)

success_chance_array = []

for learning_rate in learning_rates:
    total = 0
    successes = 0
    for training_result in sorted_training_results[learning_rate]:
        total += 1
        if training_result.status == TrainingResultStatus.SUCCESS:
            successes += 1
    success_chance_array.append(successes / total)

print(success_chance_array)

fig, ax = plt.subplots()
ax.scatter(np.array(learning_rates), np.array(success_chance_array))
plt.show()