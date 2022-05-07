class TournamentAndPatterns:
    def __init__(self, tournament, patterns, pattern_description_key, pattern_description, id = None):
        self.tournament = tournament
        self.patterns = patterns
        self.pattern_description_key = pattern_description_key
        self.pattern_description = pattern_description
        self.id = id

class ExuberantSystem:
    def __init__(self, tournament, basins):
        self.tournament = tournament
        self.basins = basins

class BasinUnderConstruction:
    def __init__(self, index, pattern_vertices, cycles, vertices_included_in_cycle):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.cycles = cycles
        self.vertices_included_in_cycle = vertices_included_in_cycle
        self.not_expandable = False
    
    def finalize(self):
        self.vertices = frozenset(self.pattern_vertices | self.vertices_included_in_cycle)

class CompletedBasin:
    def __init__(self, index, pattern_vertices, vertices):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.vertices = vertices
