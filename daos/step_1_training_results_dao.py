import daos.base_dao as base_dao
from step_1.data_structures import CalculationDurationResult, TrainingResult, TrainingResultType

def save_training_results(training_results, filename):
    serialized_training_results = list(map(_serialize_training_result, training_results))
    base_dao.add_data_no_id(serialized_training_results, filename)


def get_training_results(filename):
    serialized_training_results = base_dao.read_data(filename)
    return list(map(_deserialize_training_result, serialized_training_results))

def save_calculation_duration_results(calculation_duration_results, filename):
    serialized_results = list(map(_serialize_calculation_duration_result, calculation_duration_results))
    base_dao.add_data_no_id(serialized_results, filename)


def get_calculation_duration_results(filename):
    serialized_results = base_dao.read_data(filename)
    return list(map(_deserialize_calculation_duration_result, serialized_results))


def _deserialize_calculation_duration_result(serialized):
    type = TrainingResultType.from_id(serialized['type'])
    number_of_states = serialized['number_of_states']
    number_of_patterns = serialized['number_of_patterns']
    calculation_duration = serialized['calculation_duration']
    return CalculationDurationResult(type, number_of_states, number_of_patterns, calculation_duration)

def _serialize_calculation_duration_result(calculation_duration_result):
    serialized = {
        'type': calculation_duration_result.type.id,
        'number_of_states': calculation_duration_result.number_of_states,
        'number_of_patterns': calculation_duration_result.number_of_patterns,
        'calculation_duration': calculation_duration_result.calculation_duration
    }
    return serialized

def _serialize_training_result(training_result):
    serialized = {
        'type': training_result.type.id,
        'number_of_states': training_result.number_of_states,
        'number_of_patterns': training_result.number_of_patterns,
        'variance_of_sizes_of_basins': training_result.variance_of_sizes_of_basins
    }
    return serialized

def _deserialize_training_result(serialized):
    type = TrainingResultType.from_id(serialized['type'])
    number_of_states = serialized['number_of_states']
    number_of_patterns = serialized['number_of_patterns']
    variance_of_sizes_of_basins = serialized['variance_of_sizes_of_basins']
    return TrainingResult(type, number_of_states, number_of_patterns, variance_of_sizes_of_basins)


