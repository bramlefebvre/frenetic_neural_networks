import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
from daos.exuberant_systems_dao import get_single_exuberant_system
from step_1.moon_type_2 import find_exuberant_system
from daos.exuberant_systems_dao import save_exuberant_system
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', 'tests/data/tournaments')

exuberant_system = get_single_exuberant_system('size_8_0', 'tests/data/exuberant_systems')

pprint(exuberant_system.graph)

# exuberant_system = find_exuberant_system(tournament_and_patterns)

# pprint(exuberant_system.tournament)

print([basin.vertices for basin in exuberant_system.basins])

# exuberant_system.id = 'size_8_0'



#save_exuberant_system(exuberant_system, 'tests/data/step_1/exuberant_systems')