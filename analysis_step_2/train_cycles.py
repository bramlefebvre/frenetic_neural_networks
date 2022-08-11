import math
from analysis_step_2.data_structures import TrainingAnalysisData
from daos.exuberant_systems_dao import generate_cycle
from daos.step_2_training_analysis_data_dao import save_training_data
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.calculate_performance import calculate_performance


algorithm_2 = LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES
algorithm_3 = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC

algorithm = algorithm_3
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/algorithm_3/cv_a4x_n4x'

# (success, exuberant_system_id, number_of_states, number_of_patterns, driving_value, 
# initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, 
# training_set_size, performance):

def generate_initial_activity_parameter_factors_list(number_of_states):
    max_activity_parameter_factor = 10 * math.ceil(number_of_states / 4)
    step = 1
    if max_activity_parameter_factor > 200:
        step = math.floor(max_activity_parameter_factor / 100)
    return list(range(1, max_activity_parameter_factor + 1, step))

def generate_training_set_size_list(number_of_states):
    max_training_set_size = 10 * number_of_states
    step = 1
    if max_training_set_size > 200:
        step = math.floor(max_training_set_size / 100)
    return list(range(1, max_training_set_size, step))

def train_cycles():
    number_of_states_list = [100]
    for number_of_states in number_of_states_list:
        training_data_list = []
        cycle = generate_cycle(number_of_states)
        initial_activity_parameter_factors = [4 / 10 * number_of_states]
        for initial_activity_parameter_factor in initial_activity_parameter_factors:
            initial_dynamics = initialize_dynamics(cycle, driving_value, initial_activity_parameter_factor, travel_time)
            training_set_size_list = [4 * number_of_states]
            for training_set_size in training_set_size_list:
                print('[number_of_states, initial_activity_parameter_factor, training_set_size]:')
                print([number_of_states, initial_activity_parameter_factor, training_set_size])
                for i in range(100):
                    training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
                    if training_result.success:
                        performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
                    else: 
                        performance = None
                    training_data = TrainingAnalysisData(None, training_result.success, number_of_states, 1, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
                    training_data_list.append(training_data)
        save_training_data(training_data_list, filename)

def train_cycles_R():
    learning_rate_list = [0.5]
    number_of_states = 10
    initial_activity_parameter_factor = 4
    training_set_size = 20
    cycle = generate_cycle(number_of_states)
    initial_dynamics = initialize_dynamics(cycle, driving_value, initial_activity_parameter_factor, travel_time)
    training_data_list = []
    for learning_rate in learning_rate_list:
        print('learning_rate:')
        print(learning_rate)
        for i in range(100):
            training_result = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
            if training_result.success:
                performance = calculate_performance(training_result.dynamics, desired_residence_time, 100)
            else:
                performance = None
            training_data = TrainingAnalysisData(None, training_result.success, number_of_states, 1, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, None)
            training_data_list.append(training_data)
    save_training_data(training_data_list, filename)
