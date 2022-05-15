from daos.tournaments_and_patterns_dao import save_single_tournament_and_patterns
from step_1.data_structures import PatternDescription, TournamentAndPatterns
import numpy

a = [[-1.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
       [ 1., -1.,  1.,  0.,  0.,  1.,  0.,  0.],
       [ 1.,  0., -1.,  0.,  1.,  0.,  0.,  1.],
       [ 1.,  1.,  1., -1.,  0.,  1.,  0.,  1.],
       [ 0.,  1.,  0.,  1., -1.,  0.,  0.,  1.],
       [ 1.,  0.,  1.,  0.,  1., -1.,  1.,  1.],
       [ 1.,  1.,  1.,  1.,  1.,  0., -1.,  1.],
       [ 0.,  1.,  0.,  0.,  0.,  0.,  0., -1.]]




tournament = numpy.array(a)
tournament_and_patterns = TournamentAndPatterns(tournament, (frozenset({0}), frozenset({2})), PatternDescription.TWO_PATTERNS_EACH_WITH_ONE_STATE, 2)
save_single_tournament_and_patterns(tournament_and_patterns, 'problematic_tournaments')
