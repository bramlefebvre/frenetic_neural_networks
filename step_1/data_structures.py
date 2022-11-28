from dataclasses import dataclass
from enum import Enum, unique


class TournamentAndPatterns:
    def __init__(self, tournament, patterns, pattern_description = None, id = None):
        self.tournament = tournament
        self.patterns = patterns
        self.pattern_description = pattern_description
        self.id = id

# An ExuberantSystem is a disentangled system
class ExuberantSystem:
    def __init__(self, tournament_and_patterns_id, graph, basins, id = None):
        self.tournament_and_patterns_id = tournament_and_patterns_id
        self.graph = graph
        self.basins = basins
        self.id = id

@dataclass
class BasinUnderConstruction:
    index: int
    pattern_vertices: frozenset[int]
    cycles: set[tuple[int, ...]]
    vertices_included_in_a_cycle: set[int]
    length_of_next_cycle: int

@dataclass(frozen = True)
class CycleFindingEvent:
    basin_snapshot: BasinUnderConstruction
    new_cycle: tuple[int, ...]


@dataclass(frozen = True)
class TrainingResult:
    exuberant_system: ExuberantSystem
    cycle_finding_history: list[CycleFindingEvent]


@dataclass(frozen = True)
class CompletedBasin:
    index: int
    pattern_vertices: frozenset[int]
    vertices: frozenset[int]

@dataclass
class TrainingAnalysisData:
    number_of_states: int
    number_of_patterns: int
    sizes_of_basins: list[int] | None
    calculation_duration: float | None

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