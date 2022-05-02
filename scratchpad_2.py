import frenetic_neural_networks_io
import example1

tournament_and_patterns = {'tournament': example1.tournament, 'patterns': example1.patterns}

frenetic_neural_networks_io.write_tournament_and_patterns_array([tournament_and_patterns], 'testfile.json')