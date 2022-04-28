from find_hamilton_path import find_hamilton_path




def _find_hamilton_cycle(tournament, available_vertices):
    hamilton_path = find_hamilton_path(tournament, tuple(available_vertices))
    index = _find_largest_index_vertex_that_makes_a_cycle(tournament, hamilton_path)
    if index is None:
        return None
    cycle = list(hamilton_path[:index + 1])
    remaining_path = list(hamilton_path[index + 1:])

    while len(remaining_path) > 0:
        # extract into method
        vertex_to_add = remaining_path[0]


        
        result = _check_first_vertex_of_remaining_path_against_first_vertex_of_cycle(tournament, cycle, vertex_to_add)
        if result.fits_before:
            return InsertResult(0, [vertex_to_add])
        encountered_dominated_vertex = not result.dominates
        for index, vertex_in_cycle in enumerate(cycle[1:]):
            dominates = tournament[vertex_to_add][vertex_in_cycle] == 1
            if dominates:
                if encountered_dominated_vertex:
                    insert_result = InsertResult(index, [vertex_to_add])
                    return insert_result
            else:
                encountered_dominated_vertex = True

            

def _find_spot_to_insert_in_cycle(tournament, cycle, remaining_path):
    pass

def _check_first_vertex_of_remaining_path(tournament, cycle, vertex_to_add):
    pass 

def _check_not_first_vertex_of_remaining_path(tournament, cycle, vertex_to_add):
    pass


def _check_first_vertex_of_remaining_path_against_first_vertex_of_cycle(tournament, cycle, vertex_to_add):
    dominates = tournament[vertex_to_add][cycle[0]] == 1
    fits_before = False
    if dominates and tournament[cycle[-1]][vertex_to_add] == 1:
        fits_before = True
    return CheckAgainstFirstVertexOfCycleResult(dominates, fits_before)


def _find_largest_index_vertex_that_makes_a_cycle(tournament, hamilton_path):
    first_vertex = hamilton_path[0]
    reverse_hamilton_path = list(hamilton_path).reverse()
    for index, vertex in enumerate(reverse_hamilton_path):
        if tournament[vertex][first_vertex] == 1:
            return len(hamilton_path) - index - 1

class InsertResult:
    def __init__(self, index_to_insert_after, vertices_to_insert):
        self.index_to_insert_after = index_to_insert_after
        self.vertices_to_insert = vertices_to_insert

class CheckAgainstFirstVertexOfCycleResult:
    def __init__(self, dominates, fits_before):
        self.dominates = dominates
        self.fits_before = fits_before