'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


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
