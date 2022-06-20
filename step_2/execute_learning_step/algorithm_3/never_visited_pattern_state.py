from step_2.data_structures import Action, RateChangeInstruction
import numpy

random_number_generator = numpy.random.default_rng()

def get_rate_change_instructions(input):
    path = input.path
    graph = input.graph
    increase_rate_change_instructions = set()
    decrease_rate_change_instructions = []
    for index, state in enumerate(path):
        graph_values_for_state = graph[state, :]
        rate_change_instructions_for_state = _get_rate_change_instructions_for_state(index, state, path, graph_values_for_state)
        increase_rate_change_instructions.update(rate_change_instructions_for_state)
    all_rate_change_instructions = []
    all_rate_change_instructions.extend(decrease_rate_change_instructions)
    all_rate_change_instructions.extend(increase_rate_change_instructions)
    return all_rate_change_instructions

def _get_rate_change_instructions_for_state(index, state, path, graph_values_for_state):
    # return _increase_all_forward_arcs(state, graph_values_for_state)
    if index == len(path) - 1:
        rate_change_instructions = _increase_all_forward_arcs(state, graph_values_for_state)
    else:
        next_state_in_path = path[index + 1]
        if graph_values_for_state[next_state_in_path] == 1:
            rate_change_instructions = {RateChangeInstruction((state, next_state_in_path), Action.INCREASE)}
        else:
            rate_change_instructions = _increase_all_forward_arcs(state, graph_values_for_state)
    return rate_change_instructions

def _increase_all_forward_arcs(state, graph_values_for_state):
    rate_change_instructions = set()
    for other_state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            rate_change_instructions.add(RateChangeInstruction((state, other_state), Action.INCREASE))
    return rate_change_instructions


