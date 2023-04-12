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
import step_1.Moon_version.find_hamilton_path as find_hamilton_path
import daos.graphs_and_patterns_dao as graphs_and_patterns_dao

class FindHamiltonPathTestCase0(unittest.TestCase):

    def test_find_hamilton_path_complete_tournament(self):
        tournament_and_patterns = graphs_and_patterns_dao.get_single_graph_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.graph
        hamilton_path = find_hamilton_path.find_hamilton_path_complete_tournament(tournament)
        self.assertEqual(len(hamilton_path), 8)
        for index in range(1, len(hamilton_path)):
            self.assertEqual(tournament[hamilton_path[index - 1], hamilton_path[index]], 1)

    def test_find_hamilton_path(self):
        tournament_and_patterns = graphs_and_patterns_dao.get_single_graph_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.graph
        hamilton_path = find_hamilton_path.find_hamilton_path(tournament, [0, 1, 2, 3, 4])
        self.assertEqual(len(hamilton_path), 5)
        for index in range(1, len(hamilton_path)):
            self.assertEqual(tournament[hamilton_path[index - 1], hamilton_path[index]], 1)
            
