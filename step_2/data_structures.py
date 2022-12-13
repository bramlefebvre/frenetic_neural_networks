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


from typing import NamedTuple
from enum import Enum, unique

# immutable?
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

# immutable?
class Path:
    def __init__(self, path, residence_time_last_state):
        self.path = path
        self.residence_time_last_state = residence_time_last_state

# immutable?
class LearningStepResult:
    def __init__(self, success, rate_matrix, path, rate_change_instructions):
        self.success = success
        self.rate_matrix = rate_matrix
        self.path = path
        self.rate_change_instructions = rate_change_instructions
    
# immutable?
class LearningStepResultWithoutRateMatrix:
    def __init__(self, success, path, rate_change_instructions):
        self.success = success
        self.path = path
        self.rate_change_instructions = rate_change_instructions

@unique
class Action(Enum):
    INCREASE = 1
    DECREASE = 2

class RateChangeInstruction(NamedTuple):
    transition: tuple[int, int]
    action: Action

# immutable?
class TrainingResult:
    def __init__(self, success, dynamics, learning_step_results):
        self.success = success
        self.dynamics = dynamics
        self.learning_step_results = learning_step_results

@unique
class LearningAlgorithm(Enum):
    # THESIS = 1, 'thesis'
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
