from enum import Enum, unique
from step_2.calculate_path import calculate_path
from step_2.data_structures import Action, FailureLearningStepResult, RateChangeInstruction, SuccessLearningStepResult
from step_2.execute_learning_step import ever_left_pattern_state, never_visited_pattern_state


def execute_learning_step(dynamics, initial_state, learning_rate, desired_residence_time):
    rate_matrix = dynamics.rate_matrix.copy()
    path = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
    if path is None:
        return FailureLearningStepResult()
    basin = dynamics.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_vertices
    transitions = _to_transitions(path)
    graph = dynamics.exuberant_system.graph
    input = GetRateChangeInstructionsFunctionInput(graph, path, transitions, pattern_states)
    path_type = _determine_path_type(input, desired_residence_time)
    rate_change_instructions = rate_change_instructions_function_map[path_type](input)
    _apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate)
    return SuccessLearningStepResult(rate_matrix, path)

def _no_transitions_not_pattern_state_rate_change_instructions(input):
    last_state = input.path.path['state'][0]
    rate_change_instructions = []
    graph_values_for_last_state = input.graph[last_state, :]
    for state, graph_value in enumerate(graph_values_for_last_state):
        if graph_value == 1:
            rate_change_instructions.append(RateChangeInstruction((last_state, state), Action.INCREASE))
    return rate_change_instructions

def _no_transitions_pattern_state_rate_change_instructions(input):
    return []

def _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions(input):
    pattern_state_that_was_left = input.transitions[-1][1]
    graph_values_for_state = input.graph[pattern_state_that_was_left, :]
    rate_change_instructions = []
    for state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1:
            rate_change_instructions.append(RateChangeInstruction((pattern_state_that_was_left, state), Action.DECREASE))
    return rate_change_instructions


def _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions(input):
    return []

def _apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate):
    for rate_change_instruction in rate_change_instructions:
        transition = rate_change_instruction.transition
        factor = _get_factor_rate_change(rate_change_instruction.action, learning_rate)
        rate_matrix[transition[0], transition[1]] += factor * rate_matrix[transition[0], transition[1]]
        rate_matrix[transition[1], transition[0]] += factor * rate_matrix[transition[1], transition[0]]


def _get_factor_rate_change(action, learning_rate):
    if action == Action.INCREASE:
        factor = 1 / learning_rate - 1
    else:
        assert action == Action.DECREASE
        factor = learning_rate - 1
    return factor

def _to_transitions(path):
    path = path.path['state']
    index_last_state = len(path) - 1
    transitions = []
    for index, state in enumerate(path):
        if index != index_last_state:
            transitions.append((state, path[index + 1]))
    return transitions

def _determine_path_type(input, desired_residence_time):
    transitions = input.transitions
    if len(transitions) == 0:
        path_type = _determine_path_type_path_without_transitions(input)
    else:
        path_type = _determine_path_type_path_with_transitions(input, desired_residence_time)
    return path_type

def _determine_path_type_path_with_transitions(input, desired_residence_time):
    transitions = input.transitions
    pattern_states = input.pattern_states
    if _ever_left_pattern_state(transitions, pattern_states):
        path_type = PathType.EVER_LEFT_PATTERN_STATE
    else:
        if _arrived_in_pattern_state(transitions, pattern_states):
            if desired_residence_time <= input.path.residence_time_last_state: 
                path_type = PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH
            else:
                path_type = PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON
        else:
            path_type = PathType.NEVER_VISITED_PATTERN_STATE
    return path_type

def _determine_path_type_path_without_transitions(input):
    pattern_states = input.pattern_states
    last_state = input.path.path['state'][0]
    if last_state in pattern_states:
        path_type = PathType.NO_TRANSITIONS_PATTERN_STATE
    else:
        path_type = PathType.NO_TRANSITIONS_NOT_PATTERN_STATE
    return path_type

def _arrived_in_pattern_state(transitions, pattern_states):
    arrived_in_pattern_state = transitions[-1][1] in pattern_states
    if arrived_in_pattern_state:
        assert _other_transitions_dont_contain_pattern_states(transitions, pattern_states)
    return arrived_in_pattern_state

def _other_transitions_dont_contain_pattern_states(transitions, pattern_states):
    index_last_transition = len(transitions) - 1
    for index, transition in enumerate(transitions):
        if index != index_last_transition:
            if transition[0] in pattern_states or transition[1] in pattern_states:
                return False
    return transitions[-1][0] not in pattern_states

def _ever_left_pattern_state(transitions, pattern_states):
    for transition in transitions:
        if transition[0] in pattern_states:
            return True
    return False

class GetRateChangeInstructionsFunctionInput:
    def __init__(self, graph, path, transitions, pattern_states):
        self.graph = graph
        self.path = path
        self.transitions = transitions
        self.pattern_states = pattern_states


def _initialize_rate_change_instructions_function_map():
    rate_change_instructions_function_map = {
        PathType.EVER_LEFT_PATTERN_STATE: ever_left_pattern_state.get_rate_change_instructions,
        PathType.NEVER_VISITED_PATTERN_STATE: never_visited_pattern_state.get_rate_change_instructions,
        PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON: _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions,
        PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH: _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions,
        PathType.NO_TRANSITIONS_PATTERN_STATE: _no_transitions_pattern_state_rate_change_instructions,
        PathType.NO_TRANSITIONS_NOT_PATTERN_STATE: _no_transitions_not_pattern_state_rate_change_instructions
    }
    return rate_change_instructions_function_map

@unique
class PathType(Enum):
    ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH = 1
    EVER_LEFT_PATTERN_STATE = 2
    NEVER_VISITED_PATTERN_STATE = 3
    ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON = 4
    NO_TRANSITIONS_PATTERN_STATE = 5
    NO_TRANSITIONS_NOT_PATTERN_STATE = 6


rate_change_instructions_function_map = _initialize_rate_change_instructions_function_map()
