from find_cycle import find_cycle
from find_hamilton_cycle import hamilton_cycle_exists
import numpy

def run(tournament, patterns):
    basins = _find_cycles_per_basin(tournament, patterns)
    cycles = _gather_all_cycles(basins)
    exuberant_system = _to_exuberant_system(cycles, len(tournament))
    return MoonType2Response(exuberant_system, basins)

def _gather_all_cycles(basins):
    cycles = set()
    for basin in basins:
        cycles |= basin.cycles
    return cycles

def _to_exuberant_system(cycles, number_of_states):
    exuberant_system = -numpy.ones((number_of_states, number_of_states))
    arcs = _to_arcs(cycles)
    for arc in arcs:
        exuberant_system[arc[0]][arc[1]] = 1
        exuberant_system[arc[1]][arc[0]] = 0
    return exuberant_system

    
def _to_arcs(cycles):
    arcs = set()
    for cycle in cycles:
        for index, vertex in enumerate(cycle):
            arcs.add((cycle[index - 1], vertex))
    return arcs

def _find_cycles_per_basin(tournament, patterns):
    free_vertices = _get_initial_free_vertices(tournament, patterns)
    number_of_patterns = len(patterns)
    basins = _initialize_basins(patterns)
    pattern = 0
    while len(free_vertices) > 0:
        basin = basins[pattern]
        set_vertices_new_cycle = _expand_basin(tournament, basin, free_vertices)
        free_vertices -= set_vertices_new_cycle
        pattern = (pattern + 1) % number_of_patterns
    for basin in basins:
        basin.finalize()
    return basins
    
def _expand_basin(tournament, basin, free_vertices):
    if basin.not_expandable:
        return set()
    available_vertices = frozenset(free_vertices | basin.vertices_included_in_cycle | basin.pattern_vertices)
    if not hamilton_cycle_exists(tournament, available_vertices):
        basin.not_expandable = True
        return set()
    new_cycle = find_cycle(tournament, available_vertices, basin)
    basin.cycles |= {new_cycle}
    set_vertices_new_cycle = set(new_cycle)
    basin.vertices_included_in_cycle |= set_vertices_new_cycle
    return set_vertices_new_cycle


def _initialize_basins(patterns):
    basins = []
    for index, pattern_vertices in enumerate(patterns):
        basins.append(_initialize_basin(index, pattern_vertices))
    return tuple(basins)

def _initialize_basin(index, pattern_vertices):
    return Basin(index, frozenset(pattern_vertices), frozenset(), frozenset())

def _get_initial_free_vertices(tournament, patterns):
    all_pattern_vertices = set()
    for pattern_vertices in patterns:
        all_pattern_vertices = all_pattern_vertices | pattern_vertices
    return frozenset(range(tournament[0])) - all_pattern_vertices

class MoonType2Response:
    def __init__(self, exuberant_system, basins):
        self.exuberant_system = exuberant_system
        self.basins = basins

class Basin:
    def __init__(self, index, pattern_vertices, cycles, vertices_included_in_cycle):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.cycles = cycles
        self.vertices_included_in_cycle = vertices_included_in_cycle
        self.not_expandable = False
    
    def finalize(self):
        self.vertices = frozenset(self.pattern_vertices | self.vertices_included_in_cycle)