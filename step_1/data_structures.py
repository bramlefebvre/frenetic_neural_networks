from enum import Enum, unique


class TournamentAndPatterns:
    def __init__(self, tournament, patterns, pattern_description, id = None):
        self.tournament = tournament
        self.patterns = patterns
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

class CompletedBasin:
    def __init__(self, index, pattern_vertices, vertices):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.vertices = vertices

@unique
class PatternDescription(Enum):
    TWO_PATTERNS_EACH_WITH_ONE_STATE = 1, 'two patterns, each with one state'

    def __init__(self, id, display_value):
        self.id = id
        self.display_value = display_value

    @classmethod
    def from_id(cls, id):
        for element in list(cls):
            if element.id == id:
                return element