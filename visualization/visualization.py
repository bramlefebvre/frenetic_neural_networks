from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
from step_2.calculate_path import calculate_path
from step_2.calculate_performance import calculate_performance
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_each_vertex_n_times
from visualization.data_structures import CompleteLearningHistory, CompleteTrainingResult
import daos.complete_training_results_dao as complete_training_results_dao

filename = 'data/complete/complete_training_results'

def train_and_visualize_learning():
    pass

def train_and_save_complete_training_result():
    complete_training_result = _train()[0]
    complete_training_result.id = '8_2'
    complete_training_results_dao.save_complete_training_result(complete_training_result, filename)

def _train():
    tournament_and_patterns = generate_single_tournament_and_patterns(8, [[0], [1]])
    step_1_training_result = find_exuberant_system(tournament_and_patterns)
    exuberant_system = step_1_training_result.exuberant_system
    initial_dynamics = initialize_dynamics(exuberant_system, 5, 1, 1)
    step_2_training_result = train_starting_with_each_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_AVOID_CYCLES, 0.5, 0.2, 4)
    trained_dynamics = step_2_training_result.dynamics
    if step_2_training_result.success:
        performance = calculate_performance(trained_dynamics, 0.2, 100)
        print('performance:')
        print(performance)
    complete_training_result = CompleteTrainingResult(step_2_training_result.success, exuberant_system, trained_dynamics.rate_matrix)
    complete_learning_history = CompleteLearningHistory(step_1_training_result.cycle_finding_history, step_2_training_result.learning_step_results)
    return (complete_training_result, complete_learning_history)

def get_complete_training_result_and_visualize_recognition():
    complete_training_result = complete_training_results_dao.get_complete_training_result('8_2', filename)
    visualize_recognition(complete_training_result)

def visualize_recognition(complete_training_result):
    pass