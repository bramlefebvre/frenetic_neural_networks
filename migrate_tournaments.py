import daos.tournaments_and_patterns_dao as tournament_and_patterns_dao
import pandas

tournament_and_patterns = tournament_and_patterns_dao.get_single_tournament_and_patterns('size_20', 'tournaments')

def pprint(object):
    print(pandas.DataFrame(object))

pprint(tournament_and_patterns.tournament)