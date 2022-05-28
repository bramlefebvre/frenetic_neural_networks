from step_2.data_structures import Action, RateChangeInstruction


def get_rate_change_instructions(input):
    transitions = input.transitions
    pattern_states = input.pattern_states
    leaving_transitions = []
    for transition in transitions:
        if _is_a_leaving_transition(transition, pattern_states):
            leaving_transitions.append(transition)
    rate_change_instructions = []
    for transition in leaving_transitions:
        rate_change_instructions.append(RateChangeInstruction(transition, Action.DECREASE))
    return rate_change_instructions

def _is_a_leaving_transition(transition, pattern_states):
    return transition[0] in pattern_states