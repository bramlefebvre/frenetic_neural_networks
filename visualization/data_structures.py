from dataclasses import dataclass
from step_1.data_structures import CycleFindingEvent, ExuberantSystem
from step_2.data_structures import LearningStepResultWithoutRateMatrix
import numpy.typing as npt
from typing import Any
import numpy

@dataclass(frozen = True)
class CompleteLearningHistory:
    cycle_finding_history: list[CycleFindingEvent]
    step_2_learning_step_results: list[LearningStepResultWithoutRateMatrix]

@dataclass
class CompleteTrainingResult:
    success: bool
    exuberant_system: ExuberantSystem
    rate_matrix: npt.NDArray[numpy.double]
    id: Any = None
