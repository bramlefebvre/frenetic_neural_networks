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


import frenetic_steering.daos.graphs_and_patterns_dao as graphs_and_patterns_dao
import frenetic_steering.step_1.find_disentangled_system as find_disentangled_system
import pandas

def pprint(object):
    print(pandas.DataFrame(object))

def demo_step_1():
    number_of_vertices = 12
    serialized_patterns = [[0], [2], [3]]
    patterns = graphs_and_patterns_dao.to_tuple_of_sets(serialized_patterns)

    tournament_and_patterns = graphs_and_patterns_dao.generate_single_tournament_and_patterns(number_of_vertices, patterns)

    tournament_and_patterns = graphs_and_patterns_dao.get_single_graph_and_patterns('example_thesis', 'data/tournaments')
    disentangled_system = find_disentangled_system.find_disentangled_system(tournament_and_patterns).disentangled_system

    print('original tournament:')
    pprint(tournament_and_patterns.graph)
    print('exuberant system graph:')
    pprint(disentangled_system.graph)
    print('basins:')
    print([set(basin.vertices) for basin in disentangled_system.basins])