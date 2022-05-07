from step_2.calculate_path import calculate_path


R = 0.5

def execute_learning_step(dynamics, initial_state):
    rate_matrix = dynamics.rate_matrix.copy()
    path = calculate_path(rate_matrix, initial_state)[:, 1].tolist()
    basin = dynamics.basins.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_states
    