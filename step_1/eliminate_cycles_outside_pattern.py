import copy
from dataclasses import dataclass, field
from typing import Iterable

from step_1.data_structures import BasinUnderConstruction


def eliminate_cycles(basins: tuple[BasinUnderConstruction, ...], arcs: set[tuple[int, int]]):
    for basin in basins:
        _eliminate_cycles_for_basin(basin, arcs)


def _eliminate_cycles_for_basin(basin: BasinUnderConstruction, arcs: set[tuple[int, int]]):
    vertices_to_check: set[int] = set(basin.vertices_included_in_a_cycle - basin.pattern_vertices)
    while len(vertices_to_check) > 0:
        start_vertex: int = _pick_one(vertices_to_check)
        _eliminate_cycles_for_basin_and_start_vertex(basin, start_vertex, arcs)
        vertices_to_check.remove(start_vertex)


@dataclass
class AddVertexResult:
    success: bool = field(init = False)
    cycle: tuple[int, ...] | None

    def __post_init__(self):
        self.success = self.cycle is None

    def get_cycle(self):
        if self.cycle is None:
            raise ValueError('cycle is None')
        return self.cycle


class Walk:
    def __init__(self) -> None:
        self.walk: list[int] = []
        self.vertices: set[int] = set()

    def add_vertex(self, vertex: int) -> AddVertexResult:
        if vertex in self.vertices:
            start_index_cycle: int = self.walk.index(vertex)
            return AddVertexResult(tuple(self.walk[start_index_cycle:]))
        else: 
            self.walk.append(vertex)
            self.vertices.add(vertex)
            return AddVertexResult(None)

    def get_last_vertex(self) -> int:
        return self.walk[-1]

@dataclass
class ContinueWalkResponse:
    cycle_encountered: bool = field(init = False)
    walks: list[Walk] | None
    cycle: tuple[int, ...] | None

    def get_walks(self) -> list[Walk]:
        if self.walks is None:
            raise ValueError('walks is None')
        return self.walks
    
    def get_cycle(self) -> tuple[int, ...]:
        if self.cycle is None:
            raise ValueError('cycle is None')
        return self.cycle

    def __post__init__(self):
        self.cycle_encountered = self.cycle is not None


def _eliminate_cycles_for_basin_and_start_vertex(basin: BasinUnderConstruction, start_vertex: int, arcs: set[tuple[int, int]]):
    cycle_encountered = True
    while cycle_encountered:
        walk = Walk()
        add_vertex_result = walk.add_vertex(start_vertex)
        assert add_vertex_result.success is True
        continue_walk_response = _continue_walk(walk, basin.pattern_vertices, arcs)
        cycle_encountered = continue_walk_response.cycle_encountered
        if cycle_encountered:
            _remove_arc(continue_walk_response.get_cycle(), arcs)

            

def _continue_walk(walk: Walk, pattern_vertices, arcs) -> ContinueWalkResponse:
    new_walks: list[Walk] = []
    forward_vertices: list[int] = _forward_vertices(walk.get_last_vertex(), pattern_vertices, arcs)
    if len(forward_vertices) == 0:
        return ContinueWalkResponse([walk], None)
    for forward_vertex in forward_vertices:
        new_walk: Walk = copy.deepcopy(walk)
        add_vertex_result: AddVertexResult = new_walk.add_vertex(forward_vertex)
        if add_vertex_result.success:
            continue_walk_response: ContinueWalkResponse = _continue_walk(new_walk, pattern_vertices, arcs)
            if continue_walk_response.cycle_encountered:
                return continue_walk_response
            new_walks.extend(continue_walk_response.get_walks())
        else:
            return ContinueWalkResponse(None, add_vertex_result.get_cycle())
    return ContinueWalkResponse(new_walks, None)


def _remove_arc(cycle: tuple[int, ...], arcs: set[tuple[int, int]]):
    for index, vertex in enumerate(cycle):
        if has_outgoing_arc_going_outside_cycle(vertex, cycle, arcs):
            next_vertex = cycle[(index + 1) % len(cycle)]
            arcs.remove((vertex, next_vertex))
            return

def has_outgoing_arc_going_outside_cycle(vertex: int, cycle: tuple[int, ...], arcs: set[tuple[int, int]]):
    filtered = filter(lambda arc: arc[0] == vertex and arc[1] not in set(cycle), arcs)
    return any(filtered)

def _forward_vertices(start_vertex: int, pattern_vertices: frozenset[int], arcs: set[tuple[int, int]]) -> list[int]:
    return list(map(lambda arc: arc[1], filter(lambda arc: arc[0] == start_vertex and arc[1] not in pattern_vertices, arcs)))

def _pick_one(vertices: Iterable[int]) -> int:
    return list(vertices)[0]
