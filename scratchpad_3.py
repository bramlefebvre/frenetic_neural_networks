import numpy
import example1
from daos.generate_tournaments import to_tuple_of_sets
from step_1.moon_type_2 import run
import step_2.initialize_dynamics as initialize_dynamics

patterns = to_tuple_of_sets(example1.patterns)
tournament = numpy.array(example1.tournament)

exuberant_system = run(tournament, patterns)
print(exuberant_system.tournament)
print(initialize_dynamics.map_exuberant_system_to_dynamics(exuberant_system).rate_matrix)