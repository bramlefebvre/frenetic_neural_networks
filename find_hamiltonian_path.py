import math

def find_hamiltonian_path(tournament):
    number_of_vertices = len(tournament[0])
    hamiltonian_path = [0]
    if tournament[1][0] == 0:
        hamiltonian_path.append(1)
    else:
        hamiltonian_path.insert(0, 1)

    if tournament[2][hamiltonian_path[1]] == 0:
        hamiltonian_path.append(2)
    elif tournament[2][hamiltonian_path[0]] == 1:
        hamiltonian_path.insert(0, 2)
    else:
        hamiltonian_path.insert(1, 2)

    for vertex_to_add in range(3, number_of_vertices):
        _insert_in_path(tournament, hamiltonian_path, vertex_to_add)
    return hamiltonian_path

def _insert_in_path(tournament, hamiltonian_path, vertex_to_add):
    left_search_boundary = 0
    right_search_boundary = len(hamiltonian_path) - 1
    path_index_of_vertex_in_path = math.floor(len(hamiltonian_path)/2)
    while True:
        vertex_in_path = hamiltonian_path[path_index_of_vertex_in_path]
        if tournament[vertex_to_add][vertex_in_path] == 0:
            if path_index_of_vertex_in_path == len(hamiltonian_path) - 1:
                # success
                # end of path
                hamiltonian_path.append(vertex_to_add)
                return
            next_vertex_in_path = hamiltonian_path[path_index_of_vertex_in_path + 1]
            if tournament[vertex_to_add][next_vertex_in_path] == 1:
                # success
                # somewhere in between
                hamiltonian_path.insert(path_index_of_vertex_in_path + 1, vertex_to_add)
                return
            else:
                # search more to the right
                left_search_boundary = path_index_of_vertex_in_path
                path_index_of_vertex_in_path = math.ceil((right_search_boundary - left_search_boundary) / 2) + left_search_boundary
        else:
            if path_index_of_vertex_in_path == 0:
                # success 
                # beginning of path
                hamiltonian_path.insert(0, vertex_to_add)
                return
            # search more to the left
            right_search_boundary = path_index_of_vertex_in_path
            path_index_of_vertex_in_path = math.floor((right_search_boundary - left_search_boundary) / 2) + left_search_boundary