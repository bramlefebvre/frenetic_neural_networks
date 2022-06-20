from enum import Enum, unique
from step_2.calculate_path import calculate_path
from step_2.data_structures import Action, LearningStepResult, RateChangeInstruction
from step_2.execute_learning_step.algorithm_3 import never_visited_pattern_state

failure_learning_step_result = LearningStepResult(False, None, None, None)

def execute_learning_step(dynamics, initial_state, learning_rate, desired_residence_time):
    rate_matrix = dynamics.rate_matrix.copy()
    path = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
    if path is None:
        return failure_learning_step_result
    basin = dynamics.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_vertices
    # transitions = _to_transitions(path)
    graph = dynamics.exuberant_system.graph
    input = GetRateChangeInstructionsFunctionInput(graph, path.path['state'], pattern_states)
    path_type = _determine_path_type(input, path.path, path.residence_time_last_state, desired_residence_time)
    rate_change_instructions = rate_change_instructions_function_map[path_type](input)
    _apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate)
    return LearningStepResult(True, rate_matrix, path, rate_change_instructions)

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

def _determine_path_type(input, path_with_jump_times, residence_time_last_state, desired_residence_time):
    if _ever_left_pattern_state(input):
        path_type = PathType.EVER_LEFT_PATTERN_STATE
    else:
        if _last_state_is_a_pattern_state(input):
            residence_time_in_pattern = _residence_time_in_pattern(input, path_with_jump_times, residence_time_last_state)
            if desired_residence_time <= residence_time_in_pattern: 
                path_type = PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH
            else:
                path_type = PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON
        else:
            path_type = PathType.NEVER_VISITED_PATTERN_STATE
    return path_type

def _residence_time_in_pattern(input, path_with_jump_times, residence_time_last_state):
    index_first_pattern_state = _index_first_pattern_state(input)
    jump_time_first_pattern_state = path_with_jump_times[index_first_pattern_state]['jump_time']
    jump_time_last_state = path_with_jump_times[-1]['jump_time']
    return jump_time_last_state - jump_time_first_pattern_state + residence_time_last_state

def _index_first_pattern_state(input):
    path = input.path
    pattern_states = input.pattern_states
    for index, state in enumerate(path):
        if state in pattern_states:
            return index

def _ever_left_pattern_state(input):
    path = input.path
    pattern_states = input.pattern_states
    index_last_state = len(path) - 1
    for index, state in enumerate(path):
        if index != index_last_state:
            if state in pattern_states and path[index + 1] not in pattern_states:
                return True
    return False

def _last_state_is_a_pattern_state(input):
    return input.path[-1] in input.pattern_states

def _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions(input):
    return []

def _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions(input):
    last_state = input.path[-1]
    graph_values_for_state = input.graph[last_state, :]
    rate_change_instructions = []
    for state, graph_value in enumerate(graph_values_for_state):
        if graph_value == 1 and state not in input.pattern_states:
            rate_change_instructions.append(RateChangeInstruction((last_state, state), Action.DECREASE))
    return rate_change_instructions

def _ever_left_pattern_state_rate_change_instructions(input):
    path = input.path
    pattern_states = input.pattern_states
    graph = input.graph
    index_last_state = len(path) - 1
    rate_change_instructions = []
    for index, state in enumerate(path):
        if index != index_last_state:
            next_state_in_path = path[index + 1]
            if state in pattern_states and next_state_in_path not in pattern_states and graph[state, next_state_in_path] == 1:
                rate_change_instructions.append(RateChangeInstruction((state, path[index + 1]), Action.DECREASE))
    return rate_change_instructions

def _initialize_rate_change_instructions_function_map():
    rate_change_instructions_function_map = {
        PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH: _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions,
        PathType.EVER_LEFT_PATTERN_STATE: _ever_left_pattern_state_rate_change_instructions,
        PathType.NEVER_VISITED_PATTERN_STATE: never_visited_pattern_state.get_rate_change_instructions,
        PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON: _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions
    }
    return rate_change_instructions_function_map

class GetRateChangeInstructionsFunctionInput:
    def __init__(self, graph, path, pattern_states):
        self.graph = graph
        self.path = path
        self.pattern_states = pattern_states

@unique
class PathType(Enum):
    ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH = 1
    EVER_LEFT_PATTERN_STATE = 2
    NEVER_VISITED_PATTERN_STATE = 3
    ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON = 4

rate_change_instructions_function_map = _initialize_rate_change_instructions_function_map()