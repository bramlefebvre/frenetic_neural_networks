from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.data_structures import TrainingAnalysisData
from step_1.find_exuberant_system import find_exuberant_system
from daos.step_1_training_analysis_data_dao import save_training_data
import analysis_util




low = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
high = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

def train():
    number_of_states_list = [1000]
    # number_of_patterns_list = [5]
    for number_of_states in number_of_states_list:
        training_data_list = []
        number_of_patterns_list = analysis_util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            print('[number_of_states, number_of_patterns]:')
            print([number_of_states, number_of_patterns])
            for i in range(10):
                patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
                tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
                for j in range(10):
                    exuberant_system = find_exuberant_system(tournament_and_patterns, True).exuberant_system
                    sizes_of_basins = analysis_util.to_sizes_of_basins(exuberant_system)
                    training_data = TrainingAnalysisData(number_of_states, number_of_patterns, sizes_of_basins, None)
                    training_data_list.append(training_data)
        save_training_data(training_data_list, 'data/step_1/s1000_pv')
