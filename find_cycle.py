import numpy

random_number_generator = numpy.random.default_rng()

def find_cycle(tournament, available_vertices, pattern_vertex, cycles, used_vertices):
    unused_vertices = available_vertices - used_vertices - {pattern_vertex}

    cycle = [pattern_vertex]
    vertex_1 = _pick_one(unused_vertices)
    # first vertex always works
    if tournament[pattern_vertex][vertex_1] == 1:
        cycle.append(vertex_1)
    else:
        cycle.insert(0, vertex_1)

    possible_vertices = set(available_vertices - {pattern_vertex, vertex_1})
    if not _complete_to_3_cycle(tournament, possible_vertices, cycle):
        _complete_to_4_cycle(tournament, possible_vertices, cycle)
    return _order_cycle(cycle)


def _complete_to_4_cycle(tournament, possible_vertices, cycle):
    pass

def _complete_to_3_cycle(tournament, possible_vertices, cycle):
    vertices = possible_vertices.copy()
    found = False
    while not found:
        vertex_2 = _pick_one(vertices)
        if tournament[vertex_2][cycle[0]] == 1 and tournament[cycle[1]][vertex_2]:
            cycle.append(vertex_2)
            found = True
        else:
            vertices.remove(vertex_2)
    return found

def _order_cycle(cycle, pattern_vertex):
    pattern_vertex_index = cycle.index(pattern_vertex)
    return tuple(cycle[pattern_vertex_index:] + cycle[:pattern_vertex_index])

def _pick_one(vertices):
    return vertices[random_number_generator.integers(0, len(vertices))]






# maybe look to use used_vertices to complete cycle 
# (when you start cycle with vertex picked from unused and pattern_vertex)
# it is also possible to pick a vertex and look if it can be used to expand the length of an existing cycle

    # position_vertex_1 = cycle.index(vertex_1)
    # we can re-use one used vertex to make 3-cycle: 
    # substitute vertex_1 with vertex in existing cycle to create new cycle of same length
    # for 3-cycle (easy to generalize):
    # if position_vertex_1 = 1, then position_vertex_2 = 2 and must lose from vertex_1
    # else position_vertex_2 = 1 and must win from vertex_1
    # we're making it too difficult for the beginning just take a vertex that is not yet in the cycle
    # and check if it fits

    # we can 

    # if not possible find vertex in unused_vertices
    # unused_vertices = unused_vertices - {vertex_1}
    # first try 3-cycle


        # possibilities_third_vertices = possibilities_second_vertices.copy().remove(vertex_1)
        # for third_vertex in possibilities_third_vertices:
        #     if tournament[cycle[1]][third_vertex] == 1 and tournament[third_vertex][cycle[0]] == 1:
        #         cycle.append(third_vertex)
        #         return cycle