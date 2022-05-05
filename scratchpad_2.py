import generate_tournaments
import example1
import dao

patterns = example1.patterns
tournament = example1.tournament

new_tournament = {
            'tournament': tournament, 
            'patterns': patterns,
            'pattern_description_key': 'A'}

dao.add_data_no_duplicates([new_tournament], 'testfile_2.json')