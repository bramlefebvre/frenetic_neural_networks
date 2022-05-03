import numpy

random_number_generator = numpy.random.default_rng()

def find_cycle(tournament, available_vertices, basin):
    vertices_not_in_basin = available_vertices - basin.vertices_included_in_cycle - basin.pattern_vertices
    pattern_vertex = _pattern_vertex_least_included_in_cycle(basin)
    cycle = [pattern_vertex]
    vertex_1 = _pick_one(vertices_not_in_basin)
    # first vertex always works
    if tournament[pattern_vertex][vertex_1] == 1:
        cycle.append(vertex_1)
    else:
        cycle.insert(0, vertex_1)

    possible_vertices = available_vertices - {pattern_vertex, vertex_1}
    if not _complete_to_3_cycle(tournament, possible_vertices, cycle):
        _complete_to_4_cycle(tournament, possible_vertices, cycle)
    return _order_cycle(cycle, pattern_vertex)


def _complete_to_4_cycle(tournament, possible_vertices, cycle):
    vertices_2 = set(possible_vertices.copy())
    while True:
        vertex_2 = _pick_one(vertices_2)
        vertices_3 = set(possible_vertices.copy())
        while len(vertices_3) > 0:
            vertex_3 = _pick_one(vertices_3)
            if _check_if_completes_to_4_cycle(tournament, cycle, vertex_2, vertex_3):
                cycle.append(vertex_2)
                cycle.append(vertex_3)
                return
            else:
                vertices_3.remove(vertex_3)
        vertices_2.remove(vertex_2)

def _check_if_completes_to_4_cycle(tournament, cycle, vertex_2, vertex_3):
    return tournament[cycle[1]][vertex_2] == 1 and tournament[vertex_2][vertex_3] == 1 and \
        tournament[vertex_3][cycle[0]] == 1

def _complete_to_3_cycle(tournament, possible_vertices, cycle):
    vertices = set(possible_vertices.copy())
    found = False
    while not found and len(vertices) > 0:
        vertex_2 = _pick_one(vertices)
        if tournament[vertex_2][cycle[0]] == 1 and tournament[cycle[1]][vertex_2] == 1:
            cycle.append(vertex_2)
            found = True
        else:
            vertices.remove(vertex_2)
    return found

def _order_cycle(cycle, pattern_vertex):
    pattern_vertex_index = cycle.index(pattern_vertex)
    return tuple(cycle[pattern_vertex_index:] + cycle[:pattern_vertex_index])

def _pick_one(vertices):
    return list(vertices)[random_number_generator.integers(len(vertices))]

def _pattern_vertex_least_included_in_cycle(basin):
    pattern_vertices = basin.pattern_vertices
    number_of_times_included = {pattern_vertex: 0 for pattern_vertex in pattern_vertices}
    for cycle in basin.cycles:
        for vertex in cycle:
            if vertex in pattern_vertices:
                number_of_times_included[vertex] += 1
    return min(number_of_times_included, key = number_of_times_included.get)




# maybe look to use vertices_included_in_cycle to complete cycle 
# (when you start cycle with vertex picked from vertices_not_in_basin and pattern_vertex)

# position_vertex_1 = cycle.index(vertex_1)
# we can re-use one vertex already included in cycle to make 3-cycle: 
# substitute vertex_2 with vertex in existing cycle to create new cycle of same length
# for 3-cycle (easy to generalize):
# if position_vertex_1 = 1, then position_vertex_2 = 2 and must lose from vertex_1
# else position_vertex_2 = 1 and must win from vertex_1
# we're making it too difficult for the beginning just take a vertex that is not yet in the cycle
# and check if it fits

# it is also possible to pick a vertex and look if it can be used to expand the length of an existing cycle
