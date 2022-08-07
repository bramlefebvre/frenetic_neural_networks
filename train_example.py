from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
from step_2.calculate_performance import calculate_performance
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times

def train_example():
    patterns = (frozenset({0}),)
    tournament_and_patterns = generate_single_tournament_and_patterns(100, patterns)
    exuberant_system = find_exuberant_system(tournament_and_patterns).exuberant_system
    initial_dynamics = initialize_dynamics(exuberant_system, 5, 40, 1)
    training_result = train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 400)
    performance = calculate_performance(training_result.dynamics, 0.2, 100)
    print(performance)

train_example()
