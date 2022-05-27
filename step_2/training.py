import copy
from step_2.data_structures import FailureTrainingResult, LearningAlgorithm, SuccessTrainingResult
from step_2.execute_learning_step import algorithm_3
import step_2.execute_learning_step.algorithm_2 as algorithm_2
import step_2.execute_learning_step.algorithm_1 as algorithm_1
from step_2.calculate_path import calculate_path
import numpy

random_number_generator = numpy.random.default_rng()

algorithm_map = {
    LearningAlgorithm.THESIS: algorithm_1.execute_learning_step,
    LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES: algorithm_2.execute_learning_step,
    LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC: algorithm_3.execute_learning_step
}

def train_starting_with_each_vertex_n_times(dynamics, algorithm, learning_rate, n):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    training_set_size = n * number_of_states
    for round in range(n):
        for initial_state in range(number_of_states):
            learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate)
            if learning_step_result.success is False:
                step_number = round * number_of_states + initial_state + 1
                return FailureTrainingResult(dynamics.exuberant_system.id, dynamics.driving_value, dynamics.initial_activity_parameter_factor, dynamics.travel_time, learning_rate, algorithm, training_set_size, step_number)
            dynamics.rate_matrix = learning_step_result.rate_matrix
    performance = calculate_performance(dynamics, 100)
    return SuccessTrainingResult(dynamics.exuberant_system.id, dynamics.driving_value, dynamics.initial_activity_parameter_factor, dynamics.travel_time, learning_rate, algorithm, training_set_size, performance, dynamics.rate_matrix)

def train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, training_set_size):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    for step_number in range(training_set_size):
        initial_state = random_number_generator.choice(number_of_states)
        learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate)
        if learning_step_result.success is False:
            return FailureTrainingResult(dynamics.exuberant_system.id, dynamics.driving_value, dynamics.initial_activity_parameter_factor, dynamics.travel_time, learning_rate, algorithm, training_set_size, step_number)
        dynamics.rate_matrix = learning_step_result.rate_matrix
    performance = calculate_performance(dynamics, 100)
    return SuccessTrainingResult(dynamics.exuberant_system.id, dynamics.driving_value, dynamics.initial_activity_parameter_factor, dynamics.travel_time, learning_rate, algorithm, training_set_size, performance, dynamics.rate_matrix)


def calculate_performance(dynamics, n):
    rate_matrix = dynamics.rate_matrix
    number_of_states = len(rate_matrix)
    number_of_successes = 0
    number_of_verifications = n * number_of_states
    for _ in range(n):
        for initial_state in range(number_of_states):
            path = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
            if path is None:
                continue
            final_state_of_path = path['state'][-1]
            basin_for_state = dynamics.get_basin_for_state(initial_state)
            if final_state_of_path in basin_for_state.pattern_vertices:
                number_of_successes += 1
    return number_of_successes / number_of_verifications
