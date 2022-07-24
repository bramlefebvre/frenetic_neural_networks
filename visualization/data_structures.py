from typing import NamedTuple
from step_1.data_structures import CycleFindingEvent, ExuberantSystem
from step_2.data_structures import LearningStepResultWithoutRateMatrix

from typing import Any


# CompleteLearningHistory = namedtuple('CompleteLearningHistory', ['cycle_finding_history', 'step_2_learning_step_results'])

# CompleteTrainingResult = namedtuple('CompleteTrainingResult', ['success', 'exuberant_system', 'rate_matrix'])

class CompleteLearningHistory(NamedTuple):
    cycle_finding_history: list[CycleFindingEvent]
    step_2_learning_step_results: list[LearningStepResultWithoutRateMatrix]

# class CompleteTrainingResult(NamedTuple):
#     success: bool
#     exuberant_system: ExuberantSystem
#     rate_matrix: ndarray[float64]

# class CompleteLearningHistory:
#     def __init__(self, cycle_finding_history, step_2_learning_step_results):
#         self.cycle_finding_history = cycle_finding_history
#         self.step_2_learning_step_results = step_2_learning_step_results

class CompleteTrainingResult:
    def __init__(self, success: bool, exuberant_system, rate_matrix, id = None):
        self.success: bool = success
        self.exuberant_system = exuberant_system
        self.rate_matrix = rate_matrix
        self.id: Any = id
