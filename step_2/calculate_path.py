import numpy
from step_2.data_structures import Path

random_number_generator = numpy.random.default_rng()

def calculate_path(rate_matrix, initial_state: int, travel_time):
    number_of_states = len(rate_matrix)
    path: list[tuple[float, int]] = [(0, initial_state)]
    jump_time = 0
    state = initial_state
    residence_time: float = 0
    while jump_time < travel_time:
        if _path_is_too_long(path, number_of_states):
            return
        rates_for_state = rate_matrix[state, :]
        escape_rate = rates_for_state.sum()
        residence_time = random_number_generator.exponential(1/escape_rate)
        jump_time += residence_time
        if jump_time < travel_time:
            state = _decide_where_to_jump_to(rates_for_state, escape_rate)
            path.append((jump_time, state))
    datatype = numpy.dtype([('jump_time', float), ('state', int)])
    finished_path = numpy.array(path, datatype)
    return Path(finished_path, residence_time)


def _path_is_too_long(path, number_of_states) -> bool:
    return len(path) > 100 * number_of_states


def _decide_where_to_jump_to(rates_for_state, escape_rate) -> int:
    if escape_rate == numpy.Inf:
        return numpy.cumsum(rates_for_state).tolist().index(numpy.Inf)
    probabilities = [rate_for_state / escape_rate for rate_for_state in rates_for_state]
    return random_number_generator.choice(len(probabilities), p = probabilities)