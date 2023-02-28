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


from daos.disentangled_systems_dao import get_single_disentangled_system
import unittest
from step_2.initialize_dynamics import initialize_dynamics

class DynamicsTestCase(unittest.TestCase):

    def test_get_basin_for_state0(self):
        exuberant_system = get_single_disentangled_system('size_8_0', 'tests/data/exuberant_systems')
        dynamics = initialize_dynamics(exuberant_system, 5, 1, 1)
        self.assertEqual(dynamics.get_basin_for_state(5).index, 0)

    def test_get_basin_for_state1(self):
        exuberant_system = get_single_disentangled_system('size_8_0', 'tests/data/exuberant_systems')
        dynamics = initialize_dynamics(exuberant_system, 5, 1, 1)
        self.assertEqual(dynamics.get_basin_for_state(4).index, 1)