import numpy
import frenetic_steering.daos.base_dao as base_dao
from frenetic_steering.step_2.data_structures import RateMatrix


def get_single_rate_matrix(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return _deserialize_rate_matrix(serialized)


def save_rate_matrix(rate_matrix, filename):
    serialized = _serialize_rate_matrix(rate_matrix)
    base_dao.add_single_entry(serialized, filename)


def _serialize_rate_matrix(rate_matrix):
    serialized = {
        'id': rate_matrix.id, 
        'disentangled_system_id': rate_matrix.disentangled_system_id,
        'rate_matrix': rate_matrix.rate_matrix.tolist()
    }
    return serialized

def _deserialize_rate_matrix(serialized):
    id = serialized['id']
    disentangled_system_id = serialized['disentangled_system_id']
    rate_matrix = numpy.array(serialized['rate_matrix'], dtype = float)
    return RateMatrix(id, disentangled_system_id, rate_matrix)