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


import daos.base_dao as base_dao
from step_1.data_structures import TrainingAnalysisData

def save_training_data(training_data, filename):
    serialized_training_data = list(map(_serialize_training_data, training_data))
    base_dao.add_data_ignore_id(serialized_training_data, filename)


def get_training_data(filename):
    serialized_training_data = base_dao.read_data(filename)
    return list(map(_deserialize_training_data, serialized_training_data))

def _serialize_training_data(training_result):
    serialized = {
        'number_of_states': training_result.number_of_states,
        'number_of_patterns': training_result.number_of_patterns,
        'sizes_of_basins': training_result.sizes_of_basins,
        'calculation_duration': training_result.calculation_duration
    }
    return serialized

def _deserialize_training_data(serialized):
    number_of_states = serialized['number_of_states']
    number_of_patterns = serialized['number_of_patterns']
    sizes_of_basins = serialized['sizes_of_basins']
    calculation_duration = serialized['calculation_duration']
    return TrainingAnalysisData(number_of_states, number_of_patterns, sizes_of_basins, calculation_duration)


