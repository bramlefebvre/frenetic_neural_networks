from daos.tournaments_and_patterns import get_single_tournament_and_patterns
from step_1.moon_type_2 import find_exuberant_system
from step_2.calculate_path import calculate_path
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_each_vertex_n_times
import numpy

tournament_and_patterns = get_single_tournament_and_patterns('example_thesis', 'tournament_example_thesis.json')
exuberant_system = find_exuberant_system(tournament_and_patterns)
dynamics = initialize_dynamics(exuberant_system)

path = calculate_path(dynamics.rate_matrix, 0).tolist()
datatype = numpy.dtype([('jump_time', float), ('state', int)])
typed_path = numpy.array(path, datatype)

print(typed_path)
# dynamics = train_starting_with_each_vertex_n_times(dynamics, 3)