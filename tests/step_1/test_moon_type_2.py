import unittest
from unittest.mock import patch
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
from step_1.moon_type_2 import find_exuberant_system

filename = 'tests/data/step_1/tournaments'

class GeneralMoonType2TestCase(unittest.TestCase):

    def test_entries_are_turned_into_minus_one_or_stay_the_same(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        tournament = tournament_and_patterns.tournament
        graph = exuberant_system.tournament
        for row in range(8):
            for column in range(8):
                self.assertIn(graph[row, column], {tournament[row, column], -1}, 'problem for row: {row} and column: {column}'.format(row = str(row), column = str(column)))

    def test_only_arcs_between_vertices_of_same_basin(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        basins = exuberant_system.basins
        graph = exuberant_system.tournament
        for row in range(8):
            for column in range(8):
                if graph[row, column] != -1:
                    basin = _get_basin_for_vertex(basins, row)
                    self.assertIn(column, basin.vertices, 'problem for row: {row} and column: {column}'.format(row = str(row), column = str(column)))

    def test_at_least_one_incoming_and_one_leaving_arc(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        basins = exuberant_system.basins
        graph = exuberant_system.tournament
        if _basins_are_empty(basins):
            return
        for vertex in _non_pattern_vertices(basins):
            self.assertTrue(_incoming_arc_exists(vertex, graph), 'no incoming arc exists for vertex: {0}'.format(str(vertex)))
            self.assertTrue(_outgoing_arc_exists(vertex, graph), 'no outgoing arc exists for vertex: {0}'.format(str(vertex)))


class SpecificMoonType2TestCase(unittest.TestCase):

    @patch('step_1.moon_type_2.find_cycle')
    def test_specific_0(self, find_cycle_mock):
        find_cycle_mock.side_effect = _find_cycle_side_effect
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)

        calls = find_cycle_mock.call_args_list
        for call in calls:
            self.assertEquals(call.args[0].tolist(), tournament_and_patterns.tournament.tolist())
        self._check_first_call(calls[0])
    

    def _check_first_call(self, call):
        self.assertEqual(call.args[1], {0, 1, 3, 4, 5, 6, 7})
        basin = call.args[2]
        self.assertEqual(basin.index, 0)
    
    def _check_second_call(self, call):
        pass


def _find_cycle_side_effect(tournament, available_vertices, basin):
    cycle = ()
    if basin.index == 0:
        if len(basin.vertices_included_in_cycle) == 0:
            cycle = (0, 6, 3)
        else:
            cycle = (0, 6, 5, 3)
    else:
        if len(basin.vertices_included_in_cycle) == 0:
            cycle = (2, 4, 1)
        else:
            cycle = (2, 4, 7, 1)
    return cycle

def _outgoing_arc_exists(vertex, graph):
    for entry in graph[vertex, :]:
        if entry == 1:
            return True
    return False

def _incoming_arc_exists(vertex, graph):
    for entry in graph[vertex, :]:
        if entry == 0:
            return True
    return False
    
def _non_pattern_vertices(basins):
    non_pattern_vertices = frozenset()
    for basin in basins:
        non_pattern_vertices |= (basin.vertices - basin.pattern_vertices)
    return non_pattern_vertices

def _basins_are_empty(basins):
    for basin in basins:
        if len(basin.vertices) > len(basin.pattern_vertices):
            return False
    return True

def _get_basin_for_vertex(basins, vertex):
    for basin in basins:
        if vertex in basin.vertices:
            return basin
    
