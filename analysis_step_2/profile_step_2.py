from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
import analysis_util
import cProfile
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.data_structures import LearningAlgorithm

number_of_states = 100
number_of_patterns = 10

patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)

exuberant_system = find_exuberant_system(tournament_and_patterns, True).exuberant_system
print('exuberant system found')
initial_dynamics = initialize_dynamics(exuberant_system, 5, 5, 1)
cProfile.run('train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 400)', 'data/step_2_profiler_data_2')