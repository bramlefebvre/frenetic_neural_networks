import frenetic_neural_networks_io
import example1
import generate_tournaments

patterns_1 = generate_tournaments.to_tuple_of_sets(example1.patterns)
patterns_2 = generate_tournaments.to_tuple_of_sets(example1.patterns_2)

tournament_and_patterns_1 = {'tournament': example1.tournament, 'patterns': patterns_1}
tournament_and_patterns_2 = {'tournament': example1.tournament_2, 'patterns': patterns_2}

print(tournament_and_patterns_1 == tournament_and_patterns_2)
