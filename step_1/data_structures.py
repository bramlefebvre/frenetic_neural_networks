from enum import Enum, unique


class TournamentAndPatterns:
    def __init__(self, tournament, patterns, pattern_description = None, id = None):
        self.tournament = tournament
        self.patterns = patterns
        self.pattern_description = pattern_description
        self.id = id

class ExuberantSystem:
    def __init__(self, tournament_and_patterns_id, graph, basins, id = None):
        self.tournament_and_patterns_id = tournament_and_patterns_id
        self.graph = graph
        self.basins = basins
        self.id = id

class BasinUnderConstruction:
    def __init__(self, index, pattern_vertices, cycles, vertices_included_in_cycle, length_of_next_cycle):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.cycles = cycles
        self.vertices_included_in_cycle = vertices_included_in_cycle
        self.length_of_next_cycle = length_of_next_cycle
        self.not_expandable = False

class CompletedBasin:
    def __init__(self, index, pattern_vertices, vertices):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.vertices = vertices

class TrainingResult:
    def __init__(self, type, number_of_states, number_of_patterns, variance_of_sizes_of_basins):
        self.type = type
        self.number_of_states = number_of_states
        self.number_of_patterns = number_of_patterns
        self.variance_of_sizes_of_basins = variance_of_sizes_of_basins

class CalculationDurationResult:
    def __init__(self, type, number_of_states, number_of_patterns, calculation_duration):
        self.type = type
        self.number_of_states = number_of_states
        self.number_of_patterns = number_of_patterns
        self.calculation_duration = calculation_duration

@unique
class TrainingResultType(Enum):
    EXUBERANT_SYSTEM = 1
    TOURNAMENT = 2
    CONFIGURATION = 3

    def __init__(self, id):
        self.id = id

    @classmethod
    def from_id(cls, id):
        for element in list(cls):
            if element.id == id:
                return element    

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