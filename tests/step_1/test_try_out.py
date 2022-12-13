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
