import step_1.find_hamilton_path as find_hamilton_path
import example1
import step_1.find_hamilton_cycle as find_hamilton_cycle
import step_1.moon_type_2 as moon_type_2
import numpy
from daos.generate_tournaments import to_tuple_of_sets

patterns = to_tuple_of_sets(example1.patterns)
tournament = numpy.array(example1.tournament)

hamilton_path = find_hamilton_path.find_hamilton_path(tournament, range(len(tournament)))
hamilton_cycle = find_hamilton_cycle.find_hamilton_cycle_complete_tournament(tournament)

response = moon_type_2.run(tournament, patterns)

print('exuberant_system:')
print(response.tournament)
print('basins:')
print([basin.vertices for basin in response.basins])