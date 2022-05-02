from find_hamilton_path import find_hamilton_path


def hamilton_cycle_exists(tournament, available_vertices):
    return find_hamilton_cycle(tournament, available_vertices) is not None

def find_hamilton_cycle_complete_tournament(tournament):
    return find_hamilton_cycle(tournament, range(len(tournament)))

def find_hamilton_cycle(tournament, available_vertices):
    hamilton_path = find_hamilton_path(tournament, tuple(available_vertices))
    index = _find_largest_index_vertex_that_makes_a_cycle(tournament, hamilton_path)
    if index is None:
        return None
    cycle = list(hamilton_path[:index + 1])
    remaining_path = list(hamilton_path[index + 1:])

    while len(remaining_path) > 0:
        insert_result = _find_way_to_increase_length_cycle(tournament, cycle, remaining_path)
        if insert_result is None:
            return None
        else:
            index_to_insert_at = insert_result.index_to_insert_at
            vertices_to_insert = insert_result.vertices_to_insert
            number_of_vertices_to_insert = len(vertices_to_insert)
            assert number_of_vertices_to_insert > 0
            if number_of_vertices_to_insert == 1:
                cycle.insert(index_to_insert_at, vertices_to_insert[0])
            else:
                cycle = cycle[:index_to_insert_at] + vertices_to_insert + cycle[index_to_insert_at:]
            del remaining_path[:number_of_vertices_to_insert]
    return cycle
            

def _find_way_to_increase_length_cycle(tournament, cycle, remaining_path):
    vertex_to_insert = remaining_path[0]
    index_to_insert_at = _check_first_vertex_of_remaining_path(tournament, cycle, vertex_to_insert)
    vertices_to_insert = [vertex_to_insert]
    if index_to_insert_at is not None:
        return InsertResult(index_to_insert_at, vertices_to_insert)
    for vertex_to_insert_index in range(1, len(remaining_path)):
        vertex_to_insert = remaining_path[vertex_to_insert_index]
        index_to_insert_at = _check_not_first_vertex_of_remaining_path(tournament, cycle, vertex_to_insert)
        vertices_to_insert.append(vertex_to_insert)
        if index_to_insert_at is not None:
            return InsertResult(index_to_insert_at, vertex_to_insert)



def _check_first_vertex_of_remaining_path(tournament, cycle, vertex_to_insert):
    result = _check_first_vertex_of_remaining_path_against_first_vertex_of_cycle(tournament, cycle, vertex_to_insert)
    if result.fits_before:
        return 0
    encountered_dominating_vertex = not result.dominates
    for index, vertex_in_cycle in enumerate(cycle[1:]):
        dominates = tournament[vertex_to_insert][vertex_in_cycle] == 1
        if dominates:
            if encountered_dominating_vertex:
                return index
        else:
            encountered_dominating_vertex = True

def _check_not_first_vertex_of_remaining_path(tournament, cycle, vertex_to_insert):
    for index, vertex_in_cycle in enumerate(cycle):
        if tournament[vertex_to_insert][vertex_in_cycle] == 1:
            return index


def _check_first_vertex_of_remaining_path_against_first_vertex_of_cycle(tournament, cycle, vertex_to_insert):
    dominates = tournament[vertex_to_insert][cycle[0]] == 1
    fits_before = False
    if dominates and tournament[cycle[-1]][vertex_to_insert] == 1:
        fits_before = True
    return CheckFirstVertexOfRemainingPathAgainstFirstVertexOfCycleResult(dominates, fits_before)


def _find_largest_index_vertex_that_makes_a_cycle(tournament, hamilton_path):
    first_vertex = hamilton_path[0]
    hamilton_path_copy = list(hamilton_path)
    hamilton_path_copy.reverse()
    reverse_hamilton_path = hamilton_path_copy
    for index, vertex in enumerate(reverse_hamilton_path):
        if tournament[vertex][first_vertex] == 1:
            return len(hamilton_path) - index - 1

class InsertResult:
    def __init__(self, index_to_insert_at, vertices_to_insert):
        self.index_to_insert_at = index_to_insert_at
        self.vertices_to_insert = vertices_to_insert

class CheckFirstVertexOfRemainingPathAgainstFirstVertexOfCycleResult:
    def __init__(self, dominates, fits_before):
        self.dominates = dominates
        self.fits_before = fits_before