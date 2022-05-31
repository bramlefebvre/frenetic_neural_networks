import numpy

random_number_generator = numpy.random.default_rng()

def find_cycle(tournament, available_vertices, basin):
    pattern_vertex = _pattern_vertex_least_included_in_cycle(basin)
    possible_vertices = available_vertices - {pattern_vertex}
    if basin.length_of_next_cycle == 3:
        return tuple(_find_3_cycle(tournament, possible_vertices, pattern_vertex))
    else:
        return tuple(_find_n_cycle(tournament, possible_vertices, pattern_vertex, basin.length_of_next_cycle))

def _find_n_cycle(tournament, possible_vertices, pattern_vertex, n):
    cycle = _find_previous(tournament, possible_vertices, pattern_vertex, n)
    possible_vertices = possible_vertices - set(cycle)
    insert_result = _try_find_one_vertex_that_can_be_inserted(tournament, possible_vertices, cycle)
    if insert_result is not None:
        cycle.insert(insert_result.index_to_insert_at, insert_result.vertex_to_insert)
    else:
        two_vertices_to_be_inserted = _try_find_two_vertices_that_can_be_inserted(tournament, possible_vertices, cycle)
        del cycle[1]
        cycle.insert(1, two_vertices_to_be_inserted[1])
        cycle.insert(1, two_vertices_to_be_inserted[0])
    return _order_cycle(cycle, pattern_vertex)
    

def _try_find_two_vertices_that_can_be_inserted(tournament, possible_vertices, cycle):
    vertices_1 = set(possible_vertices)
    while True:
        vertex_1 = _pick_one(vertices_1)
        if _cycle_dominates_vertex(tournament, cycle, vertex_1):
            vertices_2 = set(possible_vertices)
            while len(vertices_2) > 0:
                vertex_2 = _pick_one(vertices_2)
                if _vertex_dominates_cycle(tournament, cycle, vertex_2) and tournament[vertex_1][vertex_2] == 1:
                    return [vertex_1, vertex_2]
                vertices_2.remove(vertex_2)
        vertices_1.remove(vertex_1)


def _vertex_dominates_cycle(tournament, cycle, vertex):
    vertex_dominates = tournament[vertex, cycle[2]] == 1
    assert _vertex_completely_dominates_cycle_if_it_dominates_third_vertex(vertex_dominates, tournament, cycle, vertex)
    return vertex_dominates

def _vertex_completely_dominates_cycle_if_it_dominates_third_vertex(vertex_dominates, tournament, cycle, vertex):
    if not vertex_dominates:
        return True
    for vertex_in_cycle in cycle:
        if tournament[vertex, vertex_in_cycle] != 1:
            return False
    return True

def _cycle_dominates_vertex(tournament, cycle, vertex):
    cycle_dominates = tournament[cycle[0], vertex] == 1
    assert _cycle_completely_dominates_vertex_if_first_vertex_dominates_it(cycle_dominates, tournament, cycle, vertex)
    return cycle_dominates

def _cycle_completely_dominates_vertex_if_first_vertex_dominates_it(cycle_dominates, tournament, cycle, vertex):
    if not cycle_dominates:
        return True
    for vertex_in_cycle in cycle:
        if tournament[vertex_in_cycle, vertex] != 1:
            return False
    return True
    

def _try_find_one_vertex_that_can_be_inserted(tournament, possible_vertices, cycle):
    vertices = set(possible_vertices)
    while len(vertices) > 0:
        vertex_to_insert = _pick_one(vertices)
        index_to_insert_at = _try_if_vertex_can_be_inserted(tournament, cycle, vertex_to_insert)
        if index_to_insert_at is not None:
            return SingleVertexInsertResult(index_to_insert_at, vertex_to_insert)
        vertices.remove(vertex_to_insert)

def _try_if_vertex_can_be_inserted(tournament, cycle, vertex_to_insert):
    result = _check_against_first_vertex_of_cycle(tournament, cycle, vertex_to_insert)
    if result.fits_before:
        return 0
    encountered_dominating_vertex_in_cycle = not result.dominates_vertex_in_cycle
    for index, vertex_in_cycle in enumerate(cycle[1:]):
        dominates = tournament[vertex_to_insert, vertex_in_cycle] == 1
        if dominates:
            if encountered_dominating_vertex_in_cycle:
                return index + 1
        else:
            encountered_dominating_vertex_in_cycle = True


def _check_against_first_vertex_of_cycle(tournament, cycle, vertex_to_insert):
    dominates_vertex_in_cycle = tournament[vertex_to_insert, cycle[0]] == 1
    fits_before = False
    if dominates_vertex_in_cycle and tournament[cycle[-1], vertex_to_insert] == 1:
        fits_before = True
    return CheckAgainstFirstVertexOfCycleResult(dominates_vertex_in_cycle, fits_before)

def _find_previous(tournament, possible_vertices, pattern_vertex, n):
    if n > 4:
        return _find_n_cycle(tournament, possible_vertices, pattern_vertex, n - 1)
    else:
        return _find_3_cycle(tournament, possible_vertices, pattern_vertex)


def _find_3_cycle(tournament, possible_vertices, pattern_vertex):
    vertices_1 = set(possible_vertices)
    while True:
        vertex_1 = _pick_one(vertices_1)
        if tournament[pattern_vertex, vertex_1] == 1:
            vertices_2 = set(possible_vertices)
            while len(vertices_2) > 0:
                vertex_2 = _pick_one(vertices_2)
                if tournament[vertex_1, vertex_2] == 1 and tournament[vertex_2, pattern_vertex] == 1:
                    return [pattern_vertex, vertex_1, vertex_2]
                else:
                    vertices_2.remove(vertex_2)
        vertices_1.remove(vertex_1)

def _order_cycle(cycle, pattern_vertex):
    pattern_vertex_index = cycle.index(pattern_vertex)
    return cycle[pattern_vertex_index:] + cycle[:pattern_vertex_index]

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

class SingleVertexInsertResult:
    def __init__(self, index_to_insert_at, vertex_to_insert):
        self.index_to_insert_at = index_to_insert_at
        self.vertex_to_insert = vertex_to_insert

class CheckAgainstFirstVertexOfCycleResult:
    def __init__(self, dominates_vertex_in_cycle, fits_before):
        self.dominates_vertex_in_cycle = dominates_vertex_in_cycle
        self.fits_before = fits_before

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
