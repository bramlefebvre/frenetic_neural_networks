from analysis_step_2.data_structures import TrainingAnalysisData
from step_2.data_structures import LearningAlgorithm
import daos.base_dao as base_dao

def save_training_data(training_data, filename):
    serialized_training_data = list(map(_serialize_training_data, training_data))
    base_dao.add_data_ignore_id(serialized_training_data, filename)

def get_training_data(filename):
    serialized_training_data = base_dao.read_data(filename)
    return list(map(_deserialize_training_data, serialized_training_data))

def _deserialize_training_data(serialized):
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
    # for backward compatibility
    if 'performance' in serialized:
        performance = serialized['performance']
    else:
        performance = None
    if 'calculation_duration' in serialized:
        calculation_duration = serialized['calculation_duration']    
    else:
        calculation_duration = None
    return TrainingAnalysisData(exuberant_system_id, success, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, performance, calculation_duration)

def _serialize_training_data(training_result):
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
        'performance': training_result.performance,
        'calculation_duration': training_result.calculation_duration
    }
    return serialized
