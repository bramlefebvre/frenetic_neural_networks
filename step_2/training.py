import copy
from step_2.data_structures import LearningAlgorithm
from step_2.execute_learning_step.algorithm_3 import algorithm_3
import numpy

random_number_generator = numpy.random.default_rng()

algorithm_map = {
    
}

def train_starting_with_each_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, n):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    for round in range(n):
        for initial_state in range(number_of_states):
            learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate, desired_residence_time)
            if learning_step_result.success is False:
                return None
            dynamics.rate_matrix = learning_step_result.rate_matrix
    return dynamics

def train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, training_set_size):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    for step_number in range(training_set_size):
        initial_state = random_number_generator.choice(number_of_states)
        learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate, desired_residence_time)
        if learning_step_result.success is False:
            return None
        dynamics.rate_matrix = learning_step_result.rate_matrix
    return dynamics
