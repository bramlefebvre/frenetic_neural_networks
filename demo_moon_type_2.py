import daos.tournaments_and_patterns_dao as tournament_and_patterns_dao
from step_1.data_structures import PatternDescription
import step_1.moon_type_2 as moon_type_2
import pandas

tournament_and_patterns = tournament_and_patterns_dao.generate_single_tournament_and_patterns(8, [[0], [2]])

exuberant_system = moon_type_2.find_exuberant_system(tournament_and_patterns)

print('original tournament')
print(tournament_and_patterns.tournament)
print('exuberant system tournament:')
print(exuberant_system.tournament)
print('basins:')
print([basin.vertices for basin in exuberant_system.basins])