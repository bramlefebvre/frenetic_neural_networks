import copy
from step_2.execute_learning_step_minimal import execute_learning_step


def train_starting_with_each_vertex_n_times(dynamics, n):
    dynamics = copy.copy(dynamics)
    number_of_states = len(dynamics.rate_matrix)
    for round in range(n):
        for initial_state in range(number_of_states):
            dynamics.rate_matrix = execute_learning_step(dynamics, initial_state)
    return dynamics
