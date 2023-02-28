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

class InitializeDynamicsTestCase(unittest.TestCase):

    def test_initialize_dynamics(self):
        exuberant_system = get_single_disentangled_system('size_8_0', 'tests/data/exuberant_systems')
        dynamics = initialize_dynamics(exuberant_system, 5, 1, 1)
        self.assertEqual(dynamics.exuberant_system, exuberant_system)
        self.assertEqual(dynamics.driving_value, 5)
        self.assertEqual(dynamics.initial_activity_parameter_factor, 1)
        self.assertEqual(dynamics.travel_time, 1)
        self._check_rate_matrix(dynamics.rate_matrix)

    def _check_rate_matrix(self, rate_matrix):
        rounded_low_value = 0.02695
        high_value = 4
        self.assertEqual(rate_matrix[0, 0], 0)
        self.assertEqual(rate_matrix[0, 1], 0)
        self.assertEqual(rate_matrix[0, 2], 0)
        self.assertEqual(round(rate_matrix[0, 3], 5), rounded_low_value)
        self.assertEqual(rate_matrix[0, 4], 0)
        self.assertEqual(rate_matrix[0, 5], 0)
        self.assertEqual(rate_matrix[0, 6], high_value)
        self.assertEqual(rate_matrix[0, 7], 0)
        self.assertEqual(rate_matrix[1, 0], 0)
        self.assertEqual(rate_matrix[1, 1], 0)
        self.assertEqual(rate_matrix[1, 2], high_value)
        self.assertEqual(rate_matrix[1, 3], 0)
        self.assertEqual(round(rate_matrix[1, 4], 5), rounded_low_value)
        self.assertEqual(rate_matrix[1, 5], 0)
        self.assertEqual(rate_matrix[1, 6], 0)
        self.assertEqual(round(rate_matrix[1, 7], 5), rounded_low_value)
        self.assertEqual(rate_matrix[2, 0], 0)
        self.assertEqual(round(rate_matrix[2, 1], 5), rounded_low_value)
        self.assertEqual(rate_matrix[2, 2], 0)
        self.assertEqual(rate_matrix[2, 3], 0)
        self.assertEqual(rate_matrix[2, 4], high_value)
        self.assertEqual(rate_matrix[2, 5], 0)
        self.assertEqual(rate_matrix[2, 6], 0)
        self.assertEqual(rate_matrix[2, 7], 0)
        self.assertEqual(rate_matrix[3, 0], high_value)
        self.assertEqual(rate_matrix[3, 1], 0)
        self.assertEqual(rate_matrix[3, 2], 0)
        self.assertEqual(rate_matrix[3, 3], 0)
        self.assertEqual(rate_matrix[3, 4], 0)
        self.assertEqual(round(rate_matrix[3, 5], 5), rounded_low_value)
        self.assertEqual(round(rate_matrix[3, 6], 5), rounded_low_value)
        self.assertEqual(rate_matrix[3, 7], 0)
        self.assertEqual(rate_matrix[4, 0], 0)
        self.assertEqual(rate_matrix[4, 1], high_value)
        self.assertEqual(round(rate_matrix[4, 2], 5), rounded_low_value)
        self.assertEqual(rate_matrix[4, 3], 0)
        self.assertEqual(rate_matrix[4, 4], 0)
        self.assertEqual(rate_matrix[4, 5], 0)
        self.assertEqual(rate_matrix[4, 6], 0)
        self.assertEqual(rate_matrix[4, 7], high_value)
        self.assertEqual(rate_matrix[5, 0], 0)
        self.assertEqual(rate_matrix[5, 1], 0)
        self.assertEqual(rate_matrix[5, 2], 0)
        self.assertEqual(rate_matrix[5, 3], high_value)
        self.assertEqual(rate_matrix[5, 4], 0)
        self.assertEqual(rate_matrix[5, 5], 0)
        self.assertEqual(round(rate_matrix[5, 6], 5), rounded_low_value)
        self.assertEqual(rate_matrix[5, 7], 0)
        self.assertEqual(round(rate_matrix[6, 0], 5), rounded_low_value)
        self.assertEqual(rate_matrix[6, 1], 0)
        self.assertEqual(rate_matrix[6, 2], 0)
        self.assertEqual(rate_matrix[6, 3], high_value)
        self.assertEqual(rate_matrix[6, 4], 0)
        self.assertEqual(rate_matrix[6, 5], high_value)
        self.assertEqual(rate_matrix[6, 6], 0)
        self.assertEqual(rate_matrix[6, 7], 0)
        self.assertEqual(rate_matrix[7, 0], 0)
        self.assertEqual(rate_matrix[7, 1], high_value)
        self.assertEqual(rate_matrix[7, 2], 0)
        self.assertEqual(rate_matrix[7, 3], 0)
        self.assertEqual(round(rate_matrix[7, 4], 5), rounded_low_value)
        self.assertEqual(rate_matrix[7, 5], 0)
        self.assertEqual(rate_matrix[7, 6], 0)
        self.assertEqual(rate_matrix[7, 7], 0)
