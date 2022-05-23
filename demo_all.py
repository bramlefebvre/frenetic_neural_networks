import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import step_1.moon_type_2 as moon_type_2
import pandas
from step_2.calculate_path import calculate_path
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training

def pprint(object):
    print(pandas.DataFrame(object))

number_of_vertices = 12
patterns = [[0], [2], [3]]
tournament_and_patterns = tournaments_and_patterns_dao.generate_single_tournament_and_patterns(number_of_vertices, patterns)
exuberant_system = moon_type_2.find_exuberant_system(tournament_and_patterns)
print('original tournament:')
pprint(tournament_and_patterns.tournament)
print('basins:')
print([basin.vertices for basin in exuberant_system.basins])
print('graph:')
pprint(exuberant_system.tournament)

travel_time = 1
driving_value = 5
initial_activity_parameter_factor = 2
learning_rate = 0.5
training_set_size = 40
algorithm = LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES

dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
print('initial rate matrix:')
pprint(dynamics.rate_matrix)

training_result = training.train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, training_set_size)
if training_result.success == True:
    initial_state = 3
    print('path:')
    print(calculate_path(training_result.rate_matrix, initial_state, travel_time))
    print('performance:')
    print(training_result.performance)
else:
    print('training failed!')