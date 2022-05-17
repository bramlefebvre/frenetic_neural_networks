import daos.exuberant_systems_dao as exuberant_systems_dao
from step_2.calculate_path import calculate_path
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

exuberant_system = exuberant_systems_dao.get_single_exuberant_system('example_thesis', 'exuberant_systems')

print([basin.vertices for basin in exuberant_system.basins])
travel_time = 1
driving_value = 5
initial_activity_parameter_factor = 1
learning_rate = 0.5

dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)

pprint(dynamics.rate_matrix)

training_set_size = 20
training_result = training.train_starting_with_random_vertex_n_times(dynamics, LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES, learning_rate, training_set_size)

print(calculate_path(training_result.rate_matrix, 5, 1))
print(training_result.performance)