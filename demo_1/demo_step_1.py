import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import step_1.find_exuberant_system as find_exuberant_system
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

number_of_vertices = 12
patterns = [[0], [2], [3]]
tournament_and_patterns = tournaments_and_patterns_dao.generate_single_tournament_and_patterns(number_of_vertices, patterns)

exuberant_system = find_exuberant_system.find_exuberant_system(tournament_and_patterns)

print('original tournament:')
pprint(tournament_and_patterns.tournament)
print('exuberant system graph:')
pprint(exuberant_system.graph)
print('basins:')
print([basin.vertices for basin in exuberant_system.basins])