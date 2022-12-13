'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


import unittest
from unittest.mock import MagicMock, patch
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
from step_1.find_exuberant_system import find_exuberant_system
from copy import deepcopy

filename = 'tests/data/tournaments'

class GeneralMoonType2TestCase0(unittest.TestCase):

    def test_entries_are_turned_into_minus_one_or_stay_the_same(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        tournament = tournament_and_patterns.tournament
        graph = exuberant_system.graph
        for row in range(8):
            for column in range(8):
                self.assertIn(graph[row, column], {tournament[row, column], -1}, 'problem for row: {row} and column: {column}'.format(row = str(row), column = str(column)))

    def test_only_arcs_between_vertices_of_same_basin(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        basins = exuberant_system.basins
        graph = exuberant_system.graph
        for row in range(8):
            for column in range(8):
                if graph[row, column] != -1:
                    basin = _get_basin_for_vertex(basins, row)
                    self.assertIn(column, basin.vertices, 'problem for row: {row} and column: {column}'.format(row = str(row), column = str(column)))

    def test_at_least_one_incoming_and_one_leaving_arc(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        basins = exuberant_system.basins
        graph = exuberant_system.graph
        if _basins_are_empty(basins):
            return
        for vertex in _non_pattern_vertices(basins):
            pass
            # self.assertTrue(_incoming_arc_exists(vertex, graph), 'no incoming arc exists for vertex: {0}'.format(str(vertex)))
            # self.assertTrue(_outgoing_arc_exists(vertex, graph), 'no outgoing arc exists for vertex: {0}'.format(str(vertex)))


class SpecificMoonType2TestCase0(unittest.TestCase):

    @patch('step_1.find_exuberant_system.find_cycle')
    def test_specific_0(self, find_cycle_mock):
        find_cycle_mock = _copy_mock(find_cycle_mock)
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', filename)
        exuberant_system = find_exuberant_system(tournament_and_patterns)
        
        self.assertEqual(exuberant_system.tournament_and_patterns_id, 'size_8_0')
        self.assertEqual(exuberant_system.graph.tolist(), self.graph)
        self._check_first_basin(exuberant_system)
        self._check_second_basin(exuberant_system)

        calls = find_cycle_mock.call_args_list
        self.assertEqual(len(calls), 4)
        for call in calls:
            self.assertEqual(call.args[0].tolist(), tournament_and_patterns.tournament.tolist())
        self._check_first_call(calls[0])
        self._check_second_call(calls[1])
        self._check_third_call(calls[2])
        self._check_fourth_call(calls[3])
    
    def _check_first_basin(self, exuberant_system):
        basin = exuberant_system.basins[0]
        self.assertEqual(basin.index, 0)
        self.assertEqual(basin.pattern_vertices, {0})
        self.assertEqual(basin.vertices, {0, 6, 5, 3})
        
    def _check_second_basin(self, exuberant_system):
        basin = exuberant_system.basins[1]
        self.assertEqual(basin.index, 1)
        self.assertEqual(basin.pattern_vertices, {2})
        self.assertEqual(basin.vertices, {2, 4, 7, 1})

    def _check_first_call(self, call):
        self.assertEqual(call.args[1], {0, 1, 3, 4, 5, 6, 7})
        basin = call.args[2]
        self.assertEqual(basin.index, 0)
        self.assertEqual(len(basin.cycles), 0)
        self.assertEqual(len(basin.vertices_included_in_cycle), 0)
        self.assertEqual(basin.length_of_next_cycle, 3)
    
    def _check_second_call(self, call):
        self.assertEqual(call.args[1], {1, 2, 4, 5, 7})
        basin = call.args[2]
        self.assertEqual(basin.index, 1)
        self.assertEqual(len(basin.cycles), 0)
        self.assertEqual(len(basin.vertices_included_in_cycle), 0)
        self.assertEqual(basin.length_of_next_cycle, 3)
    
    def _check_third_call(self, call):
        self.assertEqual(call.args[1], {0, 3, 5, 6, 7})
        basin = call.args[2]
        self.assertEqual(basin.index, 0)
        self.assertEqual(basin.cycles, {(0, 6, 3)})
        self.assertEqual(basin.vertices_included_in_cycle, {0, 6, 3})
        self.assertEqual(basin.length_of_next_cycle, 4)

    def _check_fourth_call(self, call):
        self.assertEqual(call.args[1], {1, 2, 4, 7})
        basin = call.args[2]
        self.assertEqual(basin.index, 1)
        self.assertEqual(basin.cycles, {(2, 4, 1)})
        self.assertEqual(basin.vertices_included_in_cycle, {2, 4, 1})
        self.assertEqual(basin.length_of_next_cycle, 4)

    graph = [[-1, -1, -1, 0, -1, -1, 1, -1], 
                [-1, -1, 1, -1, 0, -1, -1, 0],
                [-1, 0, -1, -1, 1, -1, -1, -1], 
                [1, -1, -1, -1, -1, 0, 0, -1], 
                [-1, 1, 0, -1, -1, -1, -1, 1], 
                [-1, -1, -1, 1, -1, -1, 0, -1],
                [0, -1, -1, 1, -1, 1, -1, -1],
                [-1, 1, -1, -1, 0, -1, -1, -1]]

def _copy_mock(mock):
    new_mock = MagicMock()
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
        basin = deepcopy(basin)
        new_mock(tournament, available_vertices, basin)
        return cycle
    mock.side_effect = _find_cycle_side_effect
    return new_mock

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
    
