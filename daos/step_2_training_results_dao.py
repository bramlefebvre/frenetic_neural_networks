from analysis_step_2.data_structures import CalculationDurationResult, TrainingResult
from step_2.data_structures import LearningAlgorithm
import daos.base_dao as base_dao

def save_training_results(training_results, filename):
    serialized_training_results = list(map(_serialize_training_result, training_results))
    base_dao.add_data_no_id(serialized_training_results, filename)

def get_training_results(filename):
    serialized_training_results = base_dao.read_data(filename)
    return list(map(_deserialize_training_result, serialized_training_results))

def save_calculation_duration_results(results, filename):
    serialized_results = list(map(_serialize_calculation_duration_result, results))
    base_dao.add_data_no_id(serialized_results, filename)

def get_calculation_duration_results(filename):
    serialized_results = base_dao.read_data(filename)
    return list(map(_deserialize_calculation_duration_result, serialized_results))

def _deserialize_calculation_duration_result(serialized):
    success = serialized['success']
    exuberant_system_id = serialized['exuberant_system_id']
    number_of_states = serialized['number_of_states']
    number_of_patterns = serialized['number_of_patterns']
    driving_value = serialized['driving_value']
    initial_activity_parameter_factor = serialized['initial_activity_parameter_factor']
    travel_time = serialized['travel_time']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    learning_rate = serialized['learning_rate']
    desired_residence_time = serialized['desired_residence_time']
    training_set_size = serialized['training_set_size']
    calculation_duration = serialized['calculation_duration']
    return CalculationDurationResult(success, exuberant_system_id, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, calculation_duration)

def _serialize_calculation_duration_result(result):
    serialized = {
        'success': result.success,
        'exuberant_system_id': result.exuberant_system_id,
        'number_of_states': result.number_of_states,
        'number_of_patterns': result.number_of_patterns,
        'driving_value': result.driving_value,
        'initial_activity_parameter_factor': result.initial_activity_parameter_factor,
        'travel_time': result.travel_time,
        'algorithm': result.algorithm.id,
        'learning_rate': result.learning_rate,
        'desired_residence_time': result.desired_residence_time,
        'training_set_size': result.training_set_size,
        'calculation_duration': result.calculation_duration
    }
    return serialized


def _deserialize_training_result(serialized):
    success = serialized['success']
    exuberant_system_id = serialized['exuberant_system_id']
    number_of_states = serialized['number_of_states']
    number_of_patterns = serialized['number_of_patterns']
    driving_value = serialized['driving_value']
    initial_activity_parameter_factor = serialized['initial_activity_parameter_factor']
    travel_time = serialized['travel_time']
    algorithm = LearningAlgorithm.from_id(serialized['algorithm'])
    learning_rate = serialized['learning_rate']
    desired_residence_time = serialized['desired_residence_time']
    training_set_size = serialized['training_set_size']
    performance = serialized['performance']
    return TrainingResult(exuberant_system_id, success, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance)

def _serialize_training_result(training_result):
    serialized = {
        'success': training_result.success,
        'exuberant_system_id': training_result.exuberant_system_id,
        'number_of_states': training_result.number_of_states,
        'number_of_patterns': training_result.number_of_patterns,
        'driving_value': training_result.driving_value,
        'initial_activity_parameter_factor': training_result.initial_activity_parameter_factor,
        'travel_time': training_result.travel_time,
        'algorithm': training_result.algorithm.id,
        'learning_rate': training_result.learning_rate,
        'desired_residence_time': training_result.desired_residence_time,
        'training_set_size': training_result.training_set_size,
        'performance': training_result.performance
    }
    return serialized
