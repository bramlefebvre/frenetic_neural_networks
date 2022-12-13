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


import math

def find_hamilton_path(tournament, available_vertices):
    hamiltonian_path = [available_vertices[0]]
    if tournament[available_vertices[1], available_vertices[0]] == 0:
        hamiltonian_path.append(available_vertices[1])
    else:
        hamiltonian_path.insert(0, available_vertices[1])

    if tournament[available_vertices[2], hamiltonian_path[1]] == 0:
        hamiltonian_path.append(available_vertices[2])
    elif tournament[available_vertices[2], hamiltonian_path[0]] == 1:
        hamiltonian_path.insert(0, available_vertices[2])
    else:
        hamiltonian_path.insert(1, available_vertices[2])

    for vertex_to_add in available_vertices[3:]:
        _insert_in_path(tournament, hamiltonian_path, vertex_to_add)
    return tuple(hamiltonian_path)

def find_hamilton_path_complete_tournament(tournament):
    return find_hamilton_path(tournament, range(len(tournament)))

def _insert_in_path(tournament, hamiltonian_path, vertex_to_add):
    left_search_boundary = 0
    right_search_boundary = len(hamiltonian_path) - 1
    path_index_of_vertex_in_path = math.floor(len(hamiltonian_path) / 2)
    while True:
        vertex_in_path = hamiltonian_path[path_index_of_vertex_in_path]
        if tournament[vertex_to_add, vertex_in_path] == 0:
            if path_index_of_vertex_in_path == len(hamiltonian_path) - 1:
                # success
                # end of path
                hamiltonian_path.append(vertex_to_add)
                return
            next_vertex_in_path = hamiltonian_path[path_index_of_vertex_in_path + 1]
            if tournament[vertex_to_add, next_vertex_in_path] == 1:
                # success
                # somewhere in between
                hamiltonian_path.insert(path_index_of_vertex_in_path + 1, vertex_to_add)
                return
            else:
                # search more to the right
                left_search_boundary = path_index_of_vertex_in_path + 1
                path_index_of_vertex_in_path = math.floor((right_search_boundary - left_search_boundary) / 2) + left_search_boundary
        else:
            if path_index_of_vertex_in_path == 0:
                # success 
                # beginning of path
                hamiltonian_path.insert(0, vertex_to_add)
                return
            # search more to the left
            right_search_boundary = path_index_of_vertex_in_path - 1
            path_index_of_vertex_in_path = math.floor((right_search_boundary - left_search_boundary) / 2) + left_search_boundary