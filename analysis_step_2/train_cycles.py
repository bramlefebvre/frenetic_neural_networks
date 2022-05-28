import math
from daos.exuberant_systems_dao import generate_cycle
from daos.step_2_training_results_dao import save_training_results
from step_2.data_structures import TrainingResult
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.calculate_performance import calculate_performance

number_of_states_list = list(range(20, 101, 10))
algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC
driving_value = 10
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/train_cycle_0'

# (self, success, exuberant_system_id, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance):

def generate_initial_activity_parameter_factors_list(number_of_states):
    max_activity_parameter_factor = 10 * math.ceil(number_of_states / 4)
    step = 1
    if max_activity_parameter_factor > 200:
        step = math.floor(max_activity_parameter_factor / 100)
    return list(range(1, max_activity_parameter_factor, step))

def generate_training_set_size_list(number_of_states):
    max_training_set_size = 10 * number_of_states
    step = 1
    if max_training_set_size > 200:
        step = math.floor(max_training_set_size / 100)
    return list(range(1, max_training_set_size, step))


def train_cycles():
    training_results = []
    for number_of_states in number_of_states_list:
        cycle = generate_cycle(number_of_states)
        initial_activity_parameter_factors = generate_initial_activity_parameter_factors_list(number_of_states)
        training_set_size_list = generate_training_set_size_list(number_of_states)
        for initial_activity_parameter_factor in initial_activity_parameter_factors:
            initial_dynamics = initialize_dynamics(cycle, driving_value, initial_activity_parameter_factor, travel_time)
            for training_set_size in training_set_size_list:
                print('[number_of_states, initial_activity_parameter_factor, training_set_size]')
                print([number_of_states, initial_activity_parameter_factor, training_set_size])
                for i in range(10):
                    trained_dynamics = train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
                    success = trained_dynamics is not None
                    if success:
                        performance = calculate_performance(trained_dynamics, desired_residence_time, 100)
                    else: 
                        performance = None
                    training_result = TrainingResult(success, None, number_of_states, 1, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance)
                    training_results.append(training_result)
        save_training_results(training_results, filename)