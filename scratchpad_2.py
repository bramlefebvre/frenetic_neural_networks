import generate_tournaments
import example1
import frenetic_neural_networks_io

patterns = example1.patterns
tournament = example1.tournament

new_tournament = {
            'tournament': tournament, 
            'patterns': patterns,
            'pattern_description_key': 'A'}

frenetic_neural_networks_io.add_data_no_duplicates([new_tournament], 'testfile_2.json')