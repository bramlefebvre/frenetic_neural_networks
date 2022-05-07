import daos.tournaments_and_patterns as tournaments_and_patterns

tournament_and_patterns = tournaments_and_patterns.get_single_tournament_and_patterns('fig.4.11', 'testfile_1.json')
print(tournament_and_patterns.tournament)
print(tournament_and_patterns.patterns)