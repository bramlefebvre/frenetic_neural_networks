from enum import Enum, unique


class Dynamics:
    def __init__(self, rate_matrix, exuberant_system, driving_value, initial_activity_parameter_factor, travel_time):
        self.rate_matrix = rate_matrix
        self.exuberant_system = exuberant_system
        self.driving_value = driving_value
        self.initial_activity_parameter_factor = initial_activity_parameter_factor
        self.travel_time = travel_time

    def get_basin_for_state(self, state):
        for basin in self.exuberant_system.basins:
            if state in basin.vertices:
                return basin

class Path:
    def __init__(self, path, residence_time_last_state):
        self.path = path
        self.residence_time_last_state = residence_time_last_state

class FailureLearningStepResult:
    def __init__(self):
        self.success = False

class SuccessLearningStepResult:
    def __init__(self, rate_matrix, path):
        self.success = True
        self.rate_matrix = rate_matrix
        self.path = path

class TrainingResult:
    def __init__(self, success, exuberant_system_id, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance):
        self.success = success
        self.exuberant_system_id = exuberant_system_id
        self.number_of_states = number_of_states
        self.number_of_patterns = number_of_patterns
        self.driving_value = driving_value
        self.initial_activity_parameter_factor = initial_activity_parameter_factor
        self.travel_time = travel_time
        self.algorithm = algorithm
        self.learning_rate = learning_rate
        self.desired_residence_time = desired_residence_time
        self.training_set_size = training_set_size
        self.performance = performance

class RateChangeInstruction:
    def __init__(self, transition, action):
        self.transition = transition
        self.action = action


@unique
class Action(Enum):
    INCREASE = 1
    DECREASE = 2


@unique
class LearningAlgorithm(Enum):
    THESIS = 1, 'thesis'
    WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES = 2, \
        'when a pattern state is left only decrease the rates for the pattern states in the path'
    LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC = 3, 'look forward and only once per arc'

    def __init__(self, id, display_value):
        self.id = id
        self.display_value = display_value

    @classmethod
    def from_id(cls, id):
        for element in list(cls):
            if element.id == id:
                return element
