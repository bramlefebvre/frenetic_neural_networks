import numpy
import example1
from daos.tournaments_and_patterns import to_tuple_of_sets
from step_1.data_structures import TournamentAndPatterns
from step_1.moon_type_2 import find_exuberant_system
import step_2.initialize_dynamics as initialize_dynamics
import daos.tournaments_and_patterns as tournaments_and_patterns

patterns = to_tuple_of_sets(example1.patterns)
tournament = numpy.array(example1.tournament)

tournament_and_patterns = TournamentAndPatterns(tournament, patterns, 'A', tournaments_and_patterns.pattern_description_map['A'], 'fig.4.11')
tournaments_and_patterns.save_single_tournament_and_patterns(tournament_and_patterns, 'testfile_1.json')

# exuberant_system = find_exuberant_system(tournament, patterns)
# print(exuberant_system.tournament)
# print(initialize_dynamics.map_exuberant_system_to_dynamics(exuberant_system).rate_matrix)