import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import step_1.find_exuberant_system as find_exuberant_system
import pandas
from step_2.calculate_path import calculate_path
from ..step_2.calculate_performance import calculate_performance
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training

def pprint(object):
    print(pandas.DataFrame(object))

def demo_all():
    number_of_vertices = 12
    serialized_patterns = [[0], [2], [3]]
    patterns = tournaments_and_patterns_dao.to_tuple_of_sets(serialized_patterns)
    tournament_and_patterns = tournaments_and_patterns_dao.generate_single_tournament_and_patterns(number_of_vertices, patterns)
    exuberant_system = find_exuberant_system.find_exuberant_system(tournament_and_patterns, False).exuberant_system
    print('original tournament:')
    pprint(tournament_and_patterns.tournament)
    print('basins:')
    print([set(basin.vertices) for basin in exuberant_system.basins])
    print('graph:')
    pprint(exuberant_system.graph)

    travel_time = 1
    driving_value = 5
    initial_activity_parameter_factor = 2
    learning_rate = 0.5
    training_set_size = 40
    desired_residence_time = 0.2

    algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC

    dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
    print('initial rate matrix:')
    pprint(dynamics.rate_matrix)

    training_result = training.train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
    if training_result.success == True:
        dynamics = training_result.dynamics
        initial_state = 5
        path = calculate_path(dynamics.rate_matrix, initial_state, travel_time)
        if path is None:
            print('unsuccessful path')
        else:
            print('path:')
            print(path.path)
            performance = calculate_performance(dynamics, desired_residence_time, 100)
            print('performance:')
            print(performance)
    else:
        print('training failed!')