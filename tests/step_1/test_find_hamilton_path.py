import unittest
import step_1.find_hamilton_path as find_hamilton_path
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao

class FindHamiltonPathTestCase0(unittest.TestCase):

    def test_find_hamilton_path_complete_tournament(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.tournament
        hamilton_path = find_hamilton_path.find_hamilton_path_complete_tournament(tournament)
        self.assertEqual(len(hamilton_path), 8)
        for index in range(1, len(hamilton_path)):
            self.assertEqual(tournament[hamilton_path[index - 1], hamilton_path[index]], 1)

    def test_find_hamilton_path(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.tournament
        hamilton_path = find_hamilton_path.find_hamilton_path(tournament, [0, 1, 2, 3, 4])
        self.assertEqual(len(hamilton_path), 5)
        for index in range(1, len(hamilton_path)):
            self.assertEqual(tournament[hamilton_path[index - 1], hamilton_path[index]], 1)
            
