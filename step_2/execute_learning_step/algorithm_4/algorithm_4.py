from enum import Enum, unique
from step_2.calculate_path import calculate_path
from step_2.data_structures import Action, LearningStepResult

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
    path_type = _determine_path_type(input, path.residence_time_last_state, desired_residence_time)
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

def _determine_path_type(input, residence_time_last_state, desired_residence_time):
    pass

def _initialize_rate_change_instructions_function_map():
    rate_change_instructions_function_map = {}
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