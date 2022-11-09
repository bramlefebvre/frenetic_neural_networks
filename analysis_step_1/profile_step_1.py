from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
import analysis_util
import cProfile

number_of_states = 1000
number_of_patterns = 100

patterns = analysis_util.generate_single_state_patterns(number_of_states, number_of_patterns)
tournament_and_patterns = generate_single_tournament_and_patterns(number_of_states, patterns)
cProfile.run('find_exuberant_system(tournament_and_patterns, True)', 'data/step_1_eliminate_cycles_profiler_data')


