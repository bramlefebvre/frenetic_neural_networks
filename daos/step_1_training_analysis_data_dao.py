import daos.base_dao as base_dao
from step_1.data_structures import TrainingAnalysisData

def save_training_data(training_data, filename):
    serialized_training_data = list(map(_serialize_training_data, training_data))
    base_dao.add_data_no_id(serialized_training_data, filename)


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


