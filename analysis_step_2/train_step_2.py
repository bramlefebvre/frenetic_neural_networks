import math
from daos.step_2_training_analysis_data_dao import save_training_data
from analysis_step_2.data_structures import TrainingAnalysisData
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.calculate_performance import calculate_performance
import analysis_util

algorithm_2 = LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES
algorithm_3 = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC


algorithm = algorithm_3
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/algorithm_3/sv_p1_a5_n4x_all_leaving'

# def _generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns):
#     fraction = 1 / 10 * number_of_states / number_of_patterns
#     return [fraction * 4]

# initial_activity_parameter_factors = [4 / 10 * number_of_states]

def _generate_initial_activity_parameter_factors_list(number_of_states):
    max_activity_parameter_factor = 10 * math.ceil(number_of_states / 4)
    step = 1
    if max_activity_parameter_factor > 200:
        step = math.floor(max_activity_parameter_factor / 100)
    return list(range(1, max_activity_parameter_factor + 1, step))

def train():
    number_of_states_list = [10 * i for i in range(1, 11)]
    for number_of_states in number_of_states_list:
        training_data_list = []
        # number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        number_of_patterns_list = [1]
        for number_of_patterns in number_of_patterns_list:
            exuberant_systems = analysis_util.generate_exuberant_systems(number_of_states, number_of_patterns, False)
            # initial_activity_parameter_factors = _generate_initial_activity_parameter_factors_list(number_of_states)
            initial_activity_parameter_factor_list = [5]
            for initial_activity_parameter_factor in initial_activity_parameter_factor_list:
                training_set_size_list = [4 * number_of_states]
                for training_set_size in training_set_size_list:
                    print('[number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size]:')
                    print([number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size])
                    for exuberant_system in exuberant_systems:
                        initial_dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
                        training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
                        if training_result.success:
                            performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
                        else: 
                            performance = None
                        training_data = TrainingAnalysisData(exuberant_system.id, training_result.success, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
                        training_data_list.append(training_data)
        save_training_data(training_data_list, filename)

def train_R():
    learning_rate_list = [0.5]
    number_of_states = 50
    number_of_patterns = 5
    initial_activity_parameter_factor = 4
    training_set_size = 200
    exuberant_systems = analysis_util.generate_exuberant_systems(number_of_states, number_of_patterns, False)
    training_data_list = []
    for learning_rate in learning_rate_list:
        print('learning_rate:')
        print(learning_rate)
        for exuberant_system in exuberant_systems:
            initial_dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
            training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
            if training_result.success:
                performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
            else:
                performance = None
            training_data = TrainingAnalysisData(None, training_result.success, number_of_states, 1, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
            training_data_list.append(training_data)
    save_training_data(training_data_list, filename)