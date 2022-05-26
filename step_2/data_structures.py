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

class FailureLearningStepResult:
    def __init__(self):
        self.success = False

class SuccessLearningStepResult:
    def __init__(self, rate_matrix, path):
        self.success = True
        self.rate_matrix = rate_matrix
        self.path = path

class SuccessTrainingResult:
    def __init__(self, exuberant_system_id, driving_value, initial_activity_parameter_factor, travel_time, learning_rate, algorithm, training_set_size, performance, rate_matrix):
        self.exuberant_system_id = exuberant_system_id
        self.success = True
        self.driving_value = driving_value
        self.initial_activity_parameter_factor = initial_activity_parameter_factor
        self.travel_time = travel_time
        self.learning_rate = learning_rate
        self.algorithm = algorithm
        self.training_set_size = training_set_size
        self.performance = performance
        self.rate_matrix = rate_matrix

class FailureTrainingResult:
    def __init__(self, exuberant_system_id, driving_value, initial_activity_parameter_factor, travel_time, learning_rate, algorithm, training_set_size, step_number):
        self.exuberant_system_id = exuberant_system_id
        self.success = False
        self.driving_value = driving_value
        self.initial_activity_parameter_factor = initial_activity_parameter_factor
        self.travel_time = travel_time
        self.learning_rate = learning_rate
        self.algorithm = algorithm
        self.training_set_size = training_set_size
        self.step_number = step_number

@unique
class LearningAlgorithm(Enum):
    THESIS = 1, 'thesis'
    WHEN_HAS_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES = 2, \
        'when a pattern state is left only decrease the rates for the pattern states in the path'

    def __init__(self, id, display_value):
        self.id = id
        self.display_value = display_value

    @classmethod
    def from_id(cls, id):
        for element in list(cls):
            if element.id == id:
                return element
