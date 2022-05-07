from step_2.calculate_path import calculate_path

R = 0.5

def execute_learning_step(dynamics, initial_state):
    rate_matrix = dynamics.rate_matrix.copy()
    path = calculate_path(rate_matrix, initial_state)[:, 1].tolist()
    basin = dynamics.basins.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_states
    if not _is_desired_path(path, pattern_states):
        _change_rates_complete_path(path, pattern_states, rate_matrix)
    return rate_matrix

def _change_rates_complete_path(path, pattern_states, rate_matrix):
    index_last_state = len(path) - 1
    for index, state in enumerate(path):
        if index != index_last_state:
            next_state = path[index + 1]
            factor = _get_factor_rate_change(state, pattern_states)
            rate_matrix[state, next_state] += factor * rate_matrix[state, next_state]
            rate_matrix[next_state, state] += factor * rate_matrix[next_state, state]

def _get_factor_rate_change(state, pattern_states):
    if state in pattern_states:
        return R - 1
    else:
        return 1 / R - 1

def _is_desired_path(path, pattern_states):
    pattern_state_indices = _indices_state_is_a_pattern_state(path, pattern_states)
    if len(pattern_state_indices) == 1 and pattern_state_indices[0] == len(path) - 1:
        return True
    else:
        return False



def _indices_state_is_a_pattern_state(path, pattern_states):
    indices = []
    for index, state in enumerate(path):
        if state in pattern_states:
            indices.append(index)
    return indices