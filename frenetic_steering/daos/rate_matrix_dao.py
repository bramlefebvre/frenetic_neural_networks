import frenetic_steering.daos.base_dao as base_dao
import numpy


def get_single_rate_matrix(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return deserialize_rate_matrix(serialized)


def save_rate_matrix(dynamics, filename):
    serialized = serialize_rate_matrix(dynamics)
    base_dao.add_single_entry(serialized, filename)

def serialize_rate_matrix(dynamics):
    serialized = {
        'rate_matrix': dynamics.rate_matrix.tolist()
    }
    return serialized

def deserialize_rate_matrix(serialized):
    rate_matrix = numpy.array(serialized['rate_matrix'], dtype = int)
    return rate_matrix