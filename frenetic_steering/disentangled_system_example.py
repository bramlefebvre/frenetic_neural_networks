'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2023 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


import numpy
import numpy.typing as npt

from step_1.data_structures import CompletedBasin, DisentangledSystem
import daos.disentangled_systems_dao as disentangled_systems_dao

graph: npt.NDArray[numpy.int_] = -numpy.ones((8, 8), dtype=int)

graph[0, 3] = 1
graph[3, 0] = 0
graph[3, 5] = 1
graph[5, 3] = 0
graph[5, 0] = 1
graph[0, 5] = 0
graph[1, 5] = 1
graph[5, 1] = 0

graph[2, 6] = 1
graph[6, 2] = 0
graph[6, 7] = 1
graph[7, 6] = 0
graph[7, 2] = 1
graph[2, 7] = 0
graph[4, 7] = 1
graph[7, 4] = 0


basin_0 = CompletedBasin(0, frozenset({0}), frozenset({0, 3, 5, 1}))
basin_1 = CompletedBasin(1, frozenset({2}), frozenset({2, 6, 7, 4}))

basins = (basin_0, basin_1)

disentangled_system = DisentangledSystem("example_thesis", graph, basins, "example_thesis")

disentangled_systems_dao.save_disentangled_system(disentangled_system, 'data/disentangled_systems')




