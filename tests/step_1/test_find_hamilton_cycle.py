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
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import step_1.find_hamilton_cycle as find_hamilton_cycle

class FindHamiltonCycleTestCase0(unittest.TestCase):

    def test_find_hamilton_cycle_complete_tournament(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.tournament
        hamilton_cycle = find_hamilton_cycle.find_hamilton_cycle_complete_tournament(tournament)
        self.assertEqual(len(hamilton_cycle), 8)
        for index, vertex in enumerate(hamilton_cycle):
            self.assertEqual(tournament[hamilton_cycle[index - 1], vertex], 1)

    def test_hamilton_cycle_does_not_exist(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.tournament
        hamilton_cycle_exists = find_hamilton_cycle.hamilton_cycle_exists(tournament, [0, 4, 5])
        self.assertFalse(hamilton_cycle_exists)

    def test_hamilton_cycle_exists(self):
        tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('size_8_0', 'tests/data/tournaments')
        tournament = tournament_and_patterns.tournament
        hamilton_cycle_exists = find_hamilton_cycle.hamilton_cycle_exists(tournament, [0, 4, 1])
        self.assertTrue(hamilton_cycle_exists)