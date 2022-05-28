from step_2.calculate_path import calculate_path

def calculate_performance(dynamics, desired_residence_time, n):
    rate_matrix = dynamics.rate_matrix
    number_of_states = len(rate_matrix)
    number_of_successes = 0
    number_of_verifications = n * number_of_states
    for _ in range(n):
        for initial_state in range(number_of_states):
            path = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
            if path is None:
                continue
            final_state_of_path = path.path['state'][-1]
            basin_for_state = dynamics.get_basin_for_state(initial_state)
            if final_state_of_path in basin_for_state.pattern_vertices and desired_residence_time <= path.residence_time_last_state:
                number_of_successes += 1
    return number_of_successes / number_of_verifications