import daos.tournaments_and_patterns as tournaments_and_patterns
import example1
import daos.base_dao as base_dao

patterns = example1.patterns
tournament = example1.tournament

new_tournament = {
            'tournament': tournament, 
            'patterns': patterns,
            'pattern_description_key': 'A'}

base_dao.add_data_no_duplicates([new_tournament], 'testfile_4.json')