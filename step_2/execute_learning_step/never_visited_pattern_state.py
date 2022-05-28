from step_2.data_structures import Action, RateChangeInstruction


def get_rate_change_instructions(input):
    transitions = set(input.transitions)
    forward_transitions = _get_forward_transitions(transitions, input.graph)
    backward_transitions = transitions - forward_transitions
    forward_arcs_from_start_states_backward_transitions = _arcs_going_forward_from_start_states_backward_transitions(backward_transitions, input.graph)
    forward_arcs_from_last_state_of_path = _arcs_going_forward_from_last_state_of_path(input)
    transitions_to_rate_change = forward_transitions | forward_arcs_from_start_states_backward_transitions | forward_arcs_from_last_state_of_path
    rate_change_instructions = []
    for transition in transitions_to_rate_change:
        rate_change_instructions.append(RateChangeInstruction(transition, Action.INCREASE))
    return rate_change_instructions

def _arcs_going_forward_from_last_state_of_path(input):
    last_state = input.transitions[-1][1]
    graph_values_for_state = input.graph[last_state, :]
    arcs = set()
    for state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            arcs.add((last_state, state))
    return arcs

def _arcs_going_forward_from_start_states_backward_transitions(backward_transitions, graph):
    start_states_backward_transitions = set()
    for backward_transition in backward_transitions:
        start_states_backward_transitions.add(backward_transition[0])
    forward_arcs = set()
    for start_state in start_states_backward_transitions:
        graph_values_from_start_state = graph[start_state, :]
        for state, graph_value in enumerate(graph_values_from_start_state):
            if graph_value == 1:
                forward_arcs.add((start_state, state))
    return forward_arcs
    
def _get_forward_transitions(transitions, graph):
    forward_transitions = set()
    for transition in transitions:
        if graph[transition[0], transition[1]] == 1:
            forward_transitions.add(transition)
    return forward_transitions