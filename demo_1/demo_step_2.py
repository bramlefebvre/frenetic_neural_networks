import daos.exuberant_systems_dao as exuberant_systems_dao
from step_2.calculate_path import calculate_path
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
import step_2.training as training
from step_2.calculate_performance import calculate_performance 
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

def demo_step_2():


    exuberant_system = exuberant_systems_dao.get_single_exuberant_system('example_thesis', 'data/exuberant_systems')

    print('basins:')
    print([set(basin.vertices) for basin in exuberant_system.basins])
    print('graph:')
    pprint(exuberant_system.graph)

    travel_time = 1
    driving_value = 5
    initial_activity_parameter_factor = 0.2
    learning_rate = 0.5
    training_set_size = 40
    desired_residence_time = 0.2
    algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC

    initial_dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)

    print('initial rate matrix:')
    pprint(initial_dynamics.rate_matrix)

    training_result = training.train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
    if training_result.success == True:
        dynamics = training_result.dynamics
        initial_state = 3
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


