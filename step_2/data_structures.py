from enum import Enum, unique


class Dynamics:
    def __init__(self, rate_matrix, exuberant_system, driving_value, travel_time):
        self.rate_matrix = rate_matrix
        self.exuberant_system = exuberant_system
        self.driving_value = driving_value
        self.travel_time = travel_time

    def get_basin_for_state(self, state):
        for basin in self.exuberant_system.basins:
            if state in basin.vertices:
                return basin

class LearningStepResult:
    def __init__(self, rate_matrix, path):
        self.rate_matrix = rate_matrix
        self.path = path

class SuccessTrainingResult:
    def __init__(self, exuberant_system_id, driving_value, travel_time, learning_rate, algorithm, training_set_size, performance, rate_matrix, id = None):
        self.exuberant_system_id = exuberant_system_id
        self.status = TrainingResultStatus.SUCCESS
        self.driving_value = driving_value
        self.travel_time = travel_time
        self.learning_rate = learning_rate
        self.algorithm = algorithm
        self.training_set_size = training_set_size
        self.performance = performance
        self.rate_matrix = rate_matrix
        self.id = id

class FailureTrainingResult:
    def __init__(self, exuberant_system_id, driving_value, travel_time, learning_rate, algorithm, step_number, id = None):
        self.exuberant_system_id = exuberant_system_id
        self.status = TrainingResultStatus.FAILURE
        self.driving_value = driving_value
        self.travel_time = travel_time
        self.learning_rate = learning_rate
        self.algorithm = algorithm
        self.step_number = step_number
        self.id = id

@unique
class TrainingResultStatus(Enum):
    SUCCESS = 1
    FAILURE = 2

@unique
class LearningAlgorithm(Enum):
    THESIS = 1, 'thesis'
    WHEN_LEFT_PATTERN_STATE_ONLY_DECREASE_RATES = 2, \
        'when a pattern state is left only decrease the rates for the pattern states in the path'

    def __init__(self, id, display_value):
        self.id = id
        self.display_value = display_value

    @classmethod
    def from_id(cls, id):
        for element in list(cls):
            if element.id == id:
                return element
