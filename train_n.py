import daos.exuberant_systems_dao as exuberant_systems_dao
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training
import daos.training_results_dao as training_results_dao

exuberant_system = exuberant_systems_dao.get_single_exuberant_system('example_thesis', 'exuberant_systems')

travel_time = 1
driving_value = 5
initial_activity_parameter_factor = 2
learning_rate = 0.5

dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)

training_results = []
for training_set_size in range(1, 21):
    for j in range(100):
        training_results.append(training.train_starting_with_random_vertex_n_times(dynamics, LearningAlgorithm.THESIS, learning_rate, training_set_size))
    
training_results_dao.save_training_results(training_results, 'algorithm_thesis/e5_a2_nv_R0.5_low')