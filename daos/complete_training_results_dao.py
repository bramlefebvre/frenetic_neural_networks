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


import numpy
import daos.base_dao as base_dao
import daos.disentangled_systems_dao as disentangled_systems_dao
from visualization.data_structures import CompleteTrainingResult

def get_complete_training_result(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return _deserialize_complete_training_result(serialized)

def save_complete_training_result(complete_training_result, filename):
    serialized = _serialize_complete_training_result(complete_training_result)
    base_dao.add_single_entry(serialized, filename)

def _serialize_complete_training_result(complete_training_result):
    serialized = {
        'success': complete_training_result.success,
        'exuberant_system': disentangled_systems_dao.serialize_disentangled_system(complete_training_result.exuberant_system),
        'rate_matrix': complete_training_result.rate_matrix.tolist()
    }
    return serialized

def _deserialize_complete_training_result(serialized):
    success = serialized['success']
    serialized_exuberant_system = serialized['exuberant_system']
    exuberant_system = disentangled_systems_dao.deserialize_disentangled_system(serialized_exuberant_system)
    rate_matrix = numpy.array(serialized['rate_matrix'])
    return CompleteTrainingResult(success, exuberant_system, rate_matrix)
    

