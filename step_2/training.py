import copy
from step_2.data_structures import LearningAlgorithm, LearningStepResultWithoutRateMatrix, TrainingResult
from step_2.execute_learning_step import algorithm_2
from step_2.execute_learning_step.algorithm_3 import algorithm_3
import numpy

random_number_generator = numpy.random.default_rng()

algorithm_map = {
    LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES: algorithm_2,
    LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC: algorithm_3.execute_learning_step
}

def train_starting_with_each_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, n):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    learning_step_results = []
    for round in range(n):
        for initial_state in range(number_of_states):
            learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate, desired_residence_time)
            learning_step_results.append(_to_learning_step_result_without_rate_matrix(learning_step_result))
            if not learning_step_result.success:
                return TrainingResult(False, dynamics, learning_step_results)
            dynamics.rate_matrix = learning_step_result.rate_matrix
    return TrainingResult(True, dynamics, learning_step_results)

def train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, training_set_size):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    learning_step_results = []
    for step_number in range(training_set_size):
        initial_state = random_number_generator.choice(number_of_states)
        learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate, desired_residence_time)
        learning_step_results.append(_to_learning_step_result_without_rate_matrix(learning_step_result))
        if not learning_step_result.success:
            return TrainingResult(False, dynamics, learning_step_results)
        dynamics.rate_matrix = learning_step_result.rate_matrix
    return TrainingResult(True, dynamics, learning_step_results)

def _to_learning_step_result_without_rate_matrix(learning_step_result):
    return LearningStepResultWithoutRateMatrix(learning_step_result.success, learning_step_result.path, learning_step_result.rate_change_instructions)
