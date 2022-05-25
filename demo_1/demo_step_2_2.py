import daos.exuberant_systems_dao as exuberant_systems_dao
from step_2.calculate_path import calculate_path
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

exuberant_system = exuberant_systems_dao.get_single_exuberant_system('size_20', 'data/exuberant_systems')

print('basins:')
print([basin.vertices for basin in exuberant_system.basins])
print('graph:')
pprint(exuberant_system.graph)

travel_time = 1
driving_value = 5
initial_activity_parameter_factor = 2
learning_rate = 0.5
training_set_size = 50
algorithm = LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES

dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)

print('initial rate matrix:')
pprint(dynamics.rate_matrix)

training_result = training.train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, training_set_size)
if training_result.success == True:
    initial_state = 12
    print('path:')
    print(calculate_path(training_result.rate_matrix, initial_state, travel_time))
    print('performance:')
    print(training_result.performance)
else:
    print('training failed!')