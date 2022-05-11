import daos.exuberant_systems_dao as exuberant_systems_dao
from step_2.data_structures import LearningAlgorithm, TrainingResultStatus
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training
import daos.training_results_dao as training_results_dao

exuberant_system = exuberant_systems_dao.get_single_exuberant_system('example_thesis', 'exuberant_systems')
dynamics = initialize_dynamics(exuberant_system, 5, 1)

# 100 times for each value of R, R starting from 0.1 to 0.9 with steps of 0.1

training_results = []
for i in range(1, 10):
    learning_rate = 0.1 * i
    for j in range(100):
        training_results.append(training.train_starting_with_each_vertex_n_times(dynamics, 5, learning_rate, LearningAlgorithm.WHEN_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES))

training_results_dao.save_training_results(training_results, 'training_results_R')