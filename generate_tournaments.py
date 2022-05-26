import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao

tournament_and_patterns = tournaments_and_patterns_dao.generate_single_tournament_and_patterns(1000, [[0]])
print('done')

# tournaments_and_patterns_dao.save_single_tournament_and_patterns(tournament_and_patterns, 'data/step_1/tournament_10000_500')

# tournaments = [tournaments_and_patterns_dao.generate_single_tournament_and_single_state_patterns(10, 1) for i in range(10)]

# print([tournament.pattern_description for tournament in tournaments])

