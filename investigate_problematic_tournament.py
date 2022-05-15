from daos.tournaments_and_patterns_dao import get_single_tournament_and_patterns
from step_1.find_hamilton_cycle import find_hamilton_cycle
from step_1.find_hamilton_path import find_hamilton_path
from step_1.moon_type_2 import find_exuberant_system


tournament_and_patterns = get_single_tournament_and_patterns(2, 'problematic_tournaments')

exuberant_system = find_exuberant_system(tournament_and_patterns)

print('cycle')
cycle = find_hamilton_cycle(tournament_and_patterns.tournament, [6, 0, 1, 5, 7])
print(cycle)

print(tournament_and_patterns.tournament)