import unittest
from unittest.mock import patch

from tests.step_1.try_out import b_function

def fun():
    return 4

class StubClass:

    def meth(self):
        return False

class TryOutTestCase(unittest.TestCase):
    @patch('tests.step_1.try_out.b_function')
    def test_1(self, mock_function):
        from tests.step_1.try_out import a_function
        mock_function.return_value = 4
        print(a_function())
