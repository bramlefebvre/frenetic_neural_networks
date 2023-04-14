'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2023 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


class TrainingAnalysisData:
    def __init__(self, success, number_of_states, number_of_patterns, driving_value,
                 initial_activity_parameter_factor, travel_time, algorithm, learning_rate, 
                 desired_residence_time, training_set_size, performance, calculation_duration):
        self.success = success
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
        self.calculation_duration = calculation_duration


