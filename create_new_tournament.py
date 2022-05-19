import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
from step_1.data_structures import PatternDescription
from step_1.moon_type_2 import find_exuberant_system
import daos.exuberant_systems_dao as exuberant_systems_dao
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

tournament_and_patterns = tournaments_and_patterns_dao.generate_single_tournament_and_patterns(8, [[0], [2]], PatternDescription.TWO_PATTERNS_EACH_WITH_ONE_STATE, 'size_8_0')
tournaments_and_patterns_dao.save_single_tournament_and_patterns(tournament_and_patterns, 'tests/data/step_1/tournaments')

# tournament_and_patterns = tournament_and_patterns_dao.get_single_tournament_and_patterns('size_20', 'tournaments')
# pprint(tournament_and_patterns.tournament)
# exuberant_system = find_exuberant_system(tournament_and_patterns)
# print([basin.vertices for basin in exuberant_system.basins])
# exuberant_system.id = 'size_8_0'
# exuberant_systems_dao.save_exuberant_system(exuberant_system, 'exuberant_systems')
