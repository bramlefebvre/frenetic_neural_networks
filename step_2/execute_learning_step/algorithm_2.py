from step_2.calculate_path import calculate_path
from step_2.data_structures import Action, LearningStepResult, RateChangeInstruction
from step_2.execute_learning_step.helper import GetRateChangeInstructionsFunctionInput, PathType, apply_rate_change_instructions, determine_path_type

failure_learning_step_result = LearningStepResult(False, None, None, None)

def execute_learning_step(dynamics, initial_state, learning_rate, desired_residence_time):
    rate_matrix = dynamics.rate_matrix.copy()
    path = calculate_path(rate_matrix, initial_state, dynamics.travel_time)
    if path is None:
        return failure_learning_step_result
    basin = dynamics.get_basin_for_state(initial_state)
    pattern_states = basin.pattern_vertices
    graph = dynamics.exuberant_system.graph
    input = GetRateChangeInstructionsFunctionInput(graph, path.path['state'], pattern_states)
    path_type = determine_path_type(input, path.path, path.residence_time_last_state, desired_residence_time)
    rate_change_instructions = rate_change_instructions_function_map[path_type](input)
    apply_rate_change_instructions(rate_matrix, rate_change_instructions, learning_rate)
    return LearningStepResult(True, rate_matrix, path, rate_change_instructions)
    
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
    index_last_state = len(path) - 1
    rate_change_instructions = []
    for index, state in enumerate(path):
        if index != index_last_state:
            next_state_in_path = path[index + 1]
            if state in pattern_states and next_state_in_path not in pattern_states:
                rate_change_instructions.append(RateChangeInstruction((state, path[index + 1]), Action.DECREASE))
    return rate_change_instructions

def _never_visited_pattern_state_rate_change_instructions(input):
    path = input.path
    index_last_state = len(path) - 1
    rate_change_instructions = []
    for index, state in enumerate(path):
        if index != index_last_state:
            next_state_in_path = path[index + 1]
            rate_change_instructions.append(RateChangeInstruction((state, next_state_in_path), Action.INCREASE))
    return rate_change_instructions

def _initialize_rate_change_instructions_function_map():
    rate_change_instructions_function_map = {
        PathType.ARRIVED_IN_PATTERN_STATE_AND_STAYED_LONG_ENOUGH: _arrived_in_pattern_state_and_stayed_long_enough_rate_change_instructions,
        PathType.EVER_LEFT_PATTERN_STATE: _ever_left_pattern_state_rate_change_instructions,
        PathType.NEVER_VISITED_PATTERN_STATE: _never_visited_pattern_state_rate_change_instructions,
        PathType.ARRIVED_IN_PATTERN_STATE_BUT_LEFT_TOO_SOON: _arrived_in_pattern_state_but_left_too_soon_rate_change_instructions
    }
    return rate_change_instructions_function_map

rate_change_instructions_function_map = _initialize_rate_change_instructions_function_map()
