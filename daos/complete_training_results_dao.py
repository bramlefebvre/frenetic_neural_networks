import numpy
import daos.base_dao as base_dao
import daos.exuberant_systems_dao as exuberant_systems_dao
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
        'exuberant_system': exuberant_systems_dao.serialize_exuberant_system(complete_training_result.exuberant_system),
        'rate_matrix': complete_training_result.rate_matrix.tolist()
    }
    return serialized

def _deserialize_complete_training_result(serialized):
    success = serialized['success']
    serialized_exuberant_system = serialized['exuberant_system']
    exuberant_system = exuberant_systems_dao.deserialize_exuberant_system(serialized_exuberant_system)
    rate_matrix = numpy.array(serialized['rate_matrix'])
    return CompleteTrainingResult(success, exuberant_system, rate_matrix)
    

