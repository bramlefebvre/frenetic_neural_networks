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

class CycleFindingEvent:
    def __init__(self, basin_snapshot, new_cycle):
        self.basin_snapshot = basin_snapshot
        self.new_cycle = new_cycle

class TrainingResult:
    def __init__(self, exuberant_system, cycle_finding_history):
        self.exuberant_system = exuberant_system
        self.cycle_finding_history = cycle_finding_history

class BasinUnderConstruction:
    def __init__(self, index, pattern_vertices, cycles, vertices_included_in_a_cycle, length_of_next_cycle):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.cycles = cycles
        self.vertices_included_in_a_cycle = vertices_included_in_a_cycle
        self.length_of_next_cycle = length_of_next_cycle
        self.not_expandable = False

class CompletedBasin:
    def __init__(self, index, pattern_vertices, vertices):
        self.index = index
        self.pattern_vertices = pattern_vertices
        self.vertices = vertices

class TrainingAnalysisData:
    def __init__(self, number_of_states, number_of_patterns, sizes_of_basins, calculation_duration):
        self.number_of_states = number_of_states
        self.number_of_patterns = number_of_patterns
        self.sizes_of_basins = sizes_of_basins
        self.calculation_duration = calculation_duration

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