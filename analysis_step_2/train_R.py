import daos.exuberant_systems_dao as exuberant_systems_dao
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training
import daos.training_results_dao as training_results_dao

exuberant_system = exuberant_systems_dao.get_single_exuberant_system('example_thesis', 'exuberant_systems')

travel_time = 1
driving_value = 10
initial_activity_parameter_factor = 0.5

dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)

# 100 times for each value of R, R starting from 0.1 to 0.9 with steps of 0.1

learning_rates = [0.1 * i for i in range(1, 10)]
training_results = []
for learning_rate in learning_rates:
    for j in range(100):
        training_results.append(training.train_starting_with_each_vertex_n_times(dynamics, LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES, learning_rate, 5))

training_results_dao.save_training_results(training_results, 'step_2/algorithm_2/e10_a0.5_n40_Rv')