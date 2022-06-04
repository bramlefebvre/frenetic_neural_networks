from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
from step_2.calculate_path import calculate_path
from step_2.calculate_performance import calculate_performance
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_each_vertex_n_times

def execute():
    tournament = generate_single_tournament_and_patterns(100, [[0], [1]])

    exuberant_system = find_exuberant_system(tournament).exuberant_system
    initial_dynamics = initialize_dynamics(exuberant_system, 5, 20, 1)
    training_result = train_starting_with_each_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_AVOID_CYCLES, 0.5, 0.2, 40)
    dynamics = training_result.dynamics
    performance = calculate_performance(dynamics, 0.2, 100)
    print(performance)
    print(calculate_path(dynamics.rate_matrix, 2, 1).path)