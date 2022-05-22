from daos.exuberant_systems_dao import get_single_exuberant_system
import unittest
from step_2.initialize_dynamics import initialize_dynamics

class DynamicsTestCase(unittest.TestCase):

    def test_get_basin_for_state0(self):
        exuberant_system = get_single_exuberant_system('size_8_0', 'tests/data/exuberant_systems')
        dynamics = initialize_dynamics(exuberant_system, 5, 1, 1)
        self.assertEqual(dynamics.get_basin_for_state(5).index, 0)

    def test_get_basin_for_state1(self):
        exuberant_system = get_single_exuberant_system('size_8_0', 'tests/data/exuberant_systems')
        dynamics = initialize_dynamics(exuberant_system, 5, 1, 1)
        self.assertEqual(dynamics.get_basin_for_state(4).index, 1)