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


from frenetic_steering.analysis_step_2.data_structures import TrainingAnalysisData
from frenetic_steering.step_2.data_structures import LearningAlgorithm
import frenetic_steering.daos.base_dao as base_dao

def save_training_data(training_data, filename):
    serialized_training_data = list(map(_serialize_training_data, training_data))
    base_dao.add_data_ignore_id(serialized_training_data, filename)

def get_training_data(filename):
    serialized_training_data = base_dao.read_data(filename)
    return list(map(_deserialize_training_data, serialized_training_data))

def _deserialize_training_data(serialized):
    success = serialized['success']
    number_of_states = serialized['number_of_states']
    number_of_patterns = serialized['number_of_patterns']
    driving_value = serialized['driving_value']
    initial_activity_parameter_factor = serialized['initial_activity_parameter_factor']
    travel_time = serialized['travel_time']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    learning_rate = serialized['learning_rate']
    desired_residence_time = serialized['desired_residence_time']
    training_set_size = serialized['training_set_size']
    if 'performance' in serialized:
        performance = serialized['performance']
    else:
        performance = None
    if 'calculation_duration' in serialized:
        calculation_duration = serialized['calculation_duration']    
    else:
        calculation_duration = None
    return TrainingAnalysisData(success, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, calculation_duration)

def _serialize_training_data(training_result):
    serialized = {
        'success': training_result.success,
        'number_of_states': training_result.number_of_states,
        'number_of_patterns': training_result.number_of_patterns,
        'driving_value': training_result.driving_value,
        'initial_activity_parameter_factor': training_result.initial_activity_parameter_factor,
        'travel_time': training_result.travel_time,
        'algorithm': training_result.algorithm.id,
        'learning_rate': training_result.learning_rate,
        'desired_residence_time': training_result.desired_residence_time,
        'training_set_size': training_result.training_set_size,
        'performance': training_result.performance,
        'calculation_duration': training_result.calculation_duration
    }
    return serialized
