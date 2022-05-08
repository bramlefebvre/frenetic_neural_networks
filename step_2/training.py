import copy
from step_2.execute_learning_step_minimal import execute_learning_step
from step_2.calculate_path import calculate_path

def train_starting_with_each_vertex_n_times(dynamics, n):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    for _ in range(n):
        for initial_state in range(number_of_states):
            dynamics.rate_matrix = execute_learning_step(dynamics, initial_state)
    return dynamics


def calculate_performance(dynamics, n):
    rate_matrix = dynamics.rate_matrix
    basins = dynamics.basins
    number_of_states = len(rate_matrix)
    number_of_successes = 0
    number_of_verifications = n * number_of_states
    for _ in range(n):
        for initial_state in range(number_of_states):
            final_state_of_path = calculate_path(rate_matrix, initial_state)['state'][-1]
            basin_for_state = basins.get_basin_for_state(initial_state)
            if final_state_of_path in basin_for_state.pattern_states:
                number_of_successes += 1
    return number_of_successes / number_of_verifications


