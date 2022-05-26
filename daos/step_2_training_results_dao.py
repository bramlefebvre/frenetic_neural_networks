import numpy
from step_2.data_structures import FailureTrainingResult, LearningAlgorithm, SuccessTrainingResult
import daos.base_dao as base_dao

def save_training_results(training_results, filename):
    serialized_training_results = list(map(_serialize_training_result, training_results))
    base_dao.add_data_no_id(serialized_training_results, filename)

def get_training_results(filename):
    serialized_training_results = base_dao.read_data(filename)
    return list(map(_deserialize_training_result, serialized_training_results))

def _deserialize_training_result(serialized):
    success = serialized['success']
    if success:
        return _deserialize_success_training_result(serialized)
    else:
        return _deserialize_failure_training_result(serialized)

def _deserialize_success_training_result(serialized):
    exuberant_system_id = serialized['exuberant_system_id']
    driving_value = serialized['driving_value']
    initial_activity_parameter_factor = serialized['initial_activity_parameter_factor']
    travel_time = serialized['travel_time']
    learning_rate = serialized['learning_rate']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    training_set_size = serialized['training_set_size']
    performance = serialized['performance']
    rate_matrix = numpy.array(serialized['rate_matrix'])
    return SuccessTrainingResult(exuberant_system_id, driving_value, initial_activity_parameter_factor, travel_time, learning_rate, algorithm, training_set_size, performance, rate_matrix)

def _deserialize_failure_training_result(serialized):
    exuberant_system_id = serialized['exuberant_system_id']
    driving_value = serialized['driving_value']
    initial_activity_parameter_factor = serialized['initial_activity_parameter_factor']
    travel_time = serialized['travel_time']
    learning_rate = serialized['learning_rate']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    training_set_size = serialized['training_set_size']
    step_number = serialized['step_number']
    return FailureTrainingResult(exuberant_system_id, driving_value, initial_activity_parameter_factor, travel_time, learning_rate, algorithm, training_set_size, step_number)

def _serialize_training_result(training_result):
    if training_result.success:
        return _serialize_success_training_result(training_result)
    else:
        return _serialize_failure_training_result(training_result)

def _serialize_success_training_result(training_result):
    serialized = _serialize_base_training_result(training_result)
    serialized['training_set_size'] = training_result.training_set_size
    serialized['performance'] = training_result.performance
    serialized['rate_matrix'] = training_result.rate_matrix.tolist()
    return serialized

def _serialize_failure_training_result(training_result):
    serialized = _serialize_base_training_result(training_result)
    serialized['training_set_size'] = training_result.training_set_size
    serialized['step_number'] = training_result.step_number
    return serialized

def _serialize_base_training_result(training_result):
    serialized = {
        'exuberant_system_id': training_result.exuberant_system_id,
        'success': training_result.success,
        'driving_value': training_result.driving_value,
        'initial_activity_parameter_factor': training_result.initial_activity_parameter_factor,
        'travel_time': training_result.travel_time,
        'learning_rate': training_result.learning_rate,
        'algorithm': training_result.algorithm.id
    }
    return serialized