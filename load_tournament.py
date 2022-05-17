import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import pandas
import step_1.find_hamilton_cycle

def pprint(object):
    print(pandas.DataFrame(object))

tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_20', 'tournaments')

strong = step_1.find_hamilton_cycle.hamilton_cycle_complete_tournament_exists(tournament_and_patterns.tournament)
print(strong)

pprint(tournament_and_patterns.tournament)

