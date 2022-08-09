from dataclasses import dataclass
from step_1.find_cycle import find_cycle
from step_1.find_hamilton_cycle import hamilton_cycle_exists
from step_1.data_structures import CycleFindingEvent, ExuberantSystem
from step_1.data_structures import BasinUnderConstruction
from step_1.data_structures import CompletedBasin
import numpy
import numpy.typing as npt
import copy
from step_1.data_structures import TrainingResult
from step_1.eliminate_cycles_outside_pattern import eliminate_cycles

def find_exuberant_system(tournament_and_patterns, no_cycles_outside_pattern: bool) -> TrainingResult:
    tournament: npt.NDArray[numpy.int_]  = tournament_and_patterns.tournament
    patterns = tournament_and_patterns.patterns
    basins_and_cycle_finding_history = _find_cycles_per_basin(tournament, patterns)
    basins: tuple[BasinUnderConstruction, ...] = basins_and_cycle_finding_history.basins
    exuberant_system_graph: npt.NDArray[numpy.int_] = _to_exuberant_system_graph(basins, len(tournament), no_cycles_outside_pattern)
    completed_basins = tuple(map(_to_completed_basin, basins))
    exuberant_system = ExuberantSystem(tournament_and_patterns.id, exuberant_system_graph, completed_basins)
    cycle_finding_history = basins_and_cycle_finding_history.cycle_finding_history
    return TrainingResult(exuberant_system, cycle_finding_history)

def _gather_all_cycles(basins: tuple[BasinUnderConstruction, ...]) -> set[tuple[int, ...]]:
    cycles: set[tuple[int, ...]] = set()
    for basin in basins:
        cycles.update(basin.cycles)
    return cycles

def _to_exuberant_system_graph(basins: tuple[BasinUnderConstruction, ...], number_of_states: int, no_cycles_outside_pattern: bool):
    graph: npt.NDArray[numpy.int_] = -numpy.ones((number_of_states, number_of_states), dtype=int)
    cycles: set[tuple[int, ...]] = _gather_all_cycles(basins)
    arcs: set[tuple[int, int]] = _to_arcs(cycles)
    if no_cycles_outside_pattern:
        eliminate_cycles(basins, arcs)
    for arc in arcs:
        graph[arc[0], arc[1]] = 1
        graph[arc[1], arc[0]] = 0
    return graph

def _to_arcs(cycles) -> set[tuple[int, int]]:
    arcs: set[tuple[int, int]] = set()
    for cycle in cycles:
        for index, vertex in enumerate(cycle):
            arcs.add((cycle[index - 1], vertex))
    return arcs

def _find_cycles_per_basin(tournament, patterns):
    free_vertices: set[int] = _get_initial_free_vertices(tournament, patterns)
    number_of_patterns: int = len(patterns)
    basins: tuple[BasinUnderConstruction, ...] = _initialize_basins(patterns)
    cycle_finding_history: list[CycleFindingEvent] = []
    if not _initial_basin_exists_that_has_available_vertices_that_can_make_hamilton_cycle(tournament, basins, free_vertices):
        return BasinsAndCycleFindingHistory(basins, cycle_finding_history)
    pattern: int = 0
    while len(free_vertices) > 0:
        basin: BasinUnderConstruction = basins[pattern]
        _expand_basin(tournament, basin, free_vertices, cycle_finding_history)
        pattern: int = (pattern + 1) % number_of_patterns
    return BasinsAndCycleFindingHistory(basins, cycle_finding_history)
    
def _expand_basin(tournament, basin: BasinUnderConstruction, free_vertices: set[int], cycle_finding_history: list[CycleFindingEvent]) -> None:
    available_vertices: frozenset[int] = frozenset(free_vertices | basin.vertices_included_in_a_cycle | basin.pattern_vertices)
    if len(available_vertices) < basin.length_of_next_cycle:
        return
    if not hamilton_cycle_exists(tournament, available_vertices):
        return
    new_cycle: tuple[int, ...] = find_cycle(tournament, available_vertices, basin)
    basin.length_of_next_cycle += 1
    basin.cycles.add(new_cycle)
    set_vertices_new_cycle: set[int] = set(new_cycle)
    basin.vertices_included_in_a_cycle.update(set_vertices_new_cycle)
    free_vertices.difference_update(set_vertices_new_cycle)
    cycle_finding_event: CycleFindingEvent = CycleFindingEvent(copy.deepcopy(basin), new_cycle)
    cycle_finding_history.append(cycle_finding_event)

def _initial_basin_exists_that_has_available_vertices_that_can_make_hamilton_cycle(tournament, basins, free_vertices):
    for basin in basins:
        available_vertices = free_vertices | basin.pattern_vertices
        if hamilton_cycle_exists(tournament, available_vertices):
            return True
    return False

def _initialize_basins(patterns) -> tuple[BasinUnderConstruction, ...]:
    basins: list[BasinUnderConstruction] = []
    for index, pattern_vertices in enumerate(patterns):
        basins.append(_initialize_basin(index, pattern_vertices))
    return tuple(basins)

def _initialize_basin(index: int, pattern_vertices) -> BasinUnderConstruction:
    return BasinUnderConstruction(index, pattern_vertices, set(), set(), 3)

def _get_initial_free_vertices(tournament, patterns) -> set[int]:
    all_pattern_vertices = set()
    all_pattern_vertices.update(*patterns)
    return set(range(len(tournament))) - all_pattern_vertices

def _to_completed_basin(basin):
    return CompletedBasin(basin.index, basin.pattern_vertices, frozenset(basin.pattern_vertices | basin.vertices_included_in_a_cycle))


@dataclass
class BasinsAndCycleFindingHistory:
    basins: tuple[BasinUnderConstruction, ...]
    cycle_finding_history: list[CycleFindingEvent]