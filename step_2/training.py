import copy
from step_2.data_structures import FailureTrainingResult, LearningAlgorithm, SuccessTrainingResult
import step_2.execute_learning_step_2 as execute_learning_step_2
import step_2.execute_learning_step_thesis as execute_learning_step_thesis
from step_2.calculate_path import calculate_path

algorithm_map = {
    LearningAlgorithm.THESIS: execute_learning_step_thesis.execute_learning_step,
    LearningAlgorithm.WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES: execute_learning_step_2.execute_learning_step
}

def train_starting_with_each_vertex_n_times(dynamics, n, learning_rate, algorithm):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    for round in range(n):
        for initial_state in range(number_of_states):
            learning_step_result = algorithm_map[algorithm](dynamics, initial_state, learning_rate)
            if learning_step_result.success is False:
                step_number = round * number_of_states + initial_state + 1
                return FailureTrainingResult(dynamics.exuberant_system.id, dynamics.driving_value, dynamics.initial_activity_parameter_factor, dynamics.travel_time, learning_rate, algorithm, step_number)
            dynamics.rate_matrix = learning_step_result.rate_matrix
    performance = calculate_performance(dynamics, 100)
    return SuccessTrainingResult(dynamics.exuberant_system.id, dynamics.driving_value, dynamics.initial_activity_parameter_factor, dynamics.travel_time, learning_rate, algorithm, n * number_of_states, performance, dynamics.rate_matrix)



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


