from find_cycle import find_cycle


class MoonType2:
    def __init__(self, tournament, patterns):
        self.tournament = tournament
        self.patterns = patterns



def run(tournament, patterns):
    free_vertices = _get_initial_free_vertices(tournament, patterns)
    number_of_patterns = len(patterns)
    basins = _initialize_basins(patterns)
    pattern = 0
    while len(free_vertices) > 0:
        basin = basins[pattern]
        set_vertices_new_cycle = _expand_basin(tournament, basin, free_vertices)
        free_vertices = free_vertices - set_vertices_new_cycle
        pattern = (pattern + 1) % number_of_patterns
    cycles = set()
    for basin in basins:
        cycles = cycles | basin.cycles
    return cycles

    
def _expand_basin(tournament, basin, free_vertices):
    if basin.not_expandable:
        return set()
    available_vertices = frozenset(free_vertices | basin.used_vertices | basin.pattern_vertices)
    if not _is_strong(tournament, list(available_vertices)):
        basin.not_expandable = True
        return set()
    pattern_vertex = _pattern_vertex_least_included_in_cycle(basin)
    new_cycle = find_cycle(tournament, available_vertices, pattern_vertex, basin.cycles, basin.used_vertices)
    basin.cycles = basin.cycles | {new_cycle}
    set_vertices_new_cycle = set(new_cycle)
    basin.used_vertices = basin.used_vertices | set_vertices_new_cycle
    return set_vertices_new_cycle

def _is_strong(tournament, available_vertices):

    pass

def _pattern_vertex_least_included_in_cycle(basin):
    pass

def _initialize_basins(patterns):
    return tuple(map(_initialize_basin, patterns))

def _initialize_basin(pattern_vertices):
    return Basin(frozenset(pattern_vertices), frozenset(), frozenset())

def _get_initial_free_vertices(tournament, patterns):
    all_pattern_vertices = set()
    for pattern_vertices in patterns:
        all_pattern_vertices = all_pattern_vertices | pattern_vertices
    return frozenset(range(tournament[0])) - all_pattern_vertices

class Basin:
    def __init__(self, pattern_vertices, cycles, used_vertices):
        self.pattern_vertices = pattern_vertices
        self.cycles = cycles
        self.used_vertices = used_vertices
        self.not_expandable = False