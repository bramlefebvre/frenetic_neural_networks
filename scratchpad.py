import find_hamilton_path
import example1
import find_hamilton_cycle
import moon_type_2
import numpy
from generate_tournaments import to_tuple_of_sets

patterns = to_tuple_of_sets(example1.patterns)
tournament = numpy.array(example1.tournament)

hamilton_path = find_hamilton_path.find_hamilton_path(tournament, range(len(tournament)))
hamilton_cycle = find_hamilton_cycle.find_hamilton_cycle_complete_tournament(tournament)

response = moon_type_2.run(tournament, patterns)

print('exuberant_system:')
print(response.tournament)
print('basins:')
print([basin.vertices for basin in response.basins])