from step_2.data_structures import Action, RateChangeInstruction


def get_rate_change_instructions(input):
    path = input.path
    graph = input.graph
    pattern_states = input.pattern_states
    increase_rate_change_instructions = set()
    decrease_rate_change_instructions = []
    for state in path:
        graph_values_for_state = graph[state, :]
        if _forward_arc_to_pattern_state_exists(graph_values_for_state, pattern_states):
            rate_change_instructions_for_state = _forward_arc_to_pattern_state_exists_rate_change_instructions(state, graph_values_for_state, pattern_states)
            decrease_rate_change_instructions_for_state = _get_decrease_rate_change_instructions(rate_change_instructions_for_state)
            decrease_rate_change_instructions.extend(decrease_rate_change_instructions_for_state)
            increase_rate_change_instructions_for_state = set(rate_change_instructions_for_state) - set(decrease_rate_change_instructions_for_state)
            increase_rate_change_instructions.update(increase_rate_change_instructions_for_state)
        else:
            rate_change_instructions_for_state = _no_forward_arc_to_pattern_state_exists_rate_change_instructions(state, graph_values_for_state)
            increase_rate_change_instructions.update(rate_change_instructions_for_state)
    all_rate_change_instructions = []
    all_rate_change_instructions.extend(decrease_rate_change_instructions)
    all_rate_change_instructions.extend(list(increase_rate_change_instructions))
    return all_rate_change_instructions

def _get_decrease_rate_change_instructions(rate_change_instructions):
    return list(filter(lambda x: x.action == Action.DECREASE, rate_change_instructions))

def _forward_arc_to_pattern_state_exists_rate_change_instructions(state, graph_values_for_state, pattern_states):
    rate_change_instructions = []
    for next_state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            if next_state in pattern_states:
                rate_change_instructions.append(RateChangeInstruction((state, next_state), Action.INCREASE))
            else:
                rate_change_instructions.append(RateChangeInstruction((state, next_state), Action.DECREASE))
    return rate_change_instructions

def _no_forward_arc_to_pattern_state_exists_rate_change_instructions(state, graph_values_for_state):
    rate_change_instructions = set()
    for next_state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            rate_change_instructions.add(RateChangeInstruction((state, next_state), Action.INCREASE))
    return rate_change_instructions


def _forward_arc_to_pattern_state_exists(graph_values_for_state, pattern_states):
    for next_state, graph_value in enumerate(graph_values_for_state):
        if next_state in pattern_states and graph_value == 1:
            return True
    return False


