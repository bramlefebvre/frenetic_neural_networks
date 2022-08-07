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
        forward_vertices = _forward_vertices(start_vertex, basin.pattern_vertices, arcs)
        walk = Walk([start_vertex], forward_vertices)
        _eliminate_cycles_starting_from_walk(walk, basin.pattern_vertices, arcs)
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
    def __init__(self, walk: list[int], remaining_forward_vertices: list[int] | None) -> None:
        self.walk: list[int] = walk
        self.vertices: set[int] = set(walk)
        self.remaining_forward_vertices: list[int] | None = remaining_forward_vertices

    def add_vertex(self, vertex: int) -> AddVertexResult:
        if vertex in self.vertices:
            start_index_cycle: int = self.walk.index(vertex)
            return AddVertexResult(tuple(self.walk[start_index_cycle:]))
        else: 
            self.walk.append(vertex)
            self.vertices.add(vertex)
            return AddVertexResult(None)

    def get_remaining_forward_vertices(self):
        if self.remaining_forward_vertices is None:
            raise ValueError('remaining_forward_vertices is None')
        return self.remaining_forward_vertices

@dataclass
class ContinueWalkResponse:
    cycle_encountered: bool = field(init = False)
    unfinished_walks: list[Walk] | None
    cycle: tuple[int, ...] | None

    def get_unfinished_walks(self) -> list[Walk]:
        if self.unfinished_walks is None:
            raise ValueError('walks is None')
        return self.unfinished_walks
    
    def get_cycle(self) -> tuple[int, ...]:
        if self.cycle is None:
            raise ValueError('cycle is None')
        return self.cycle

    def __post_init__(self):
        self.cycle_encountered = self.cycle is not None


# def _eliminate_cycles_for_basin_and_start_vertex(basin: BasinUnderConstruction, start_vertex: int, arcs: set[tuple[int, int]]):
#     cycle_encountered = True
#     while cycle_encountered:
#         walk = Walk()
#         add_vertex_result = walk.add_vertex(start_vertex)
#         assert add_vertex_result.success is True
#         continue_walk_response = _continue_walk(walk, basin.pattern_vertices, arcs)
#         if continue_walk_response.cycle_encountered:
#             _find_arc_to_remove(continue_walk_response.get_cycle(), arcs)

def _eliminate_cycles_starting_from_walk(walk: Walk, pattern_vertices, arcs: set[tuple[int, int]]):
    continue_walk_response = _continue_walk(walk, pattern_vertices, arcs)
    removed_arcs: set[tuple[int, int]] = set()
    if continue_walk_response.cycle_encountered:
        arc_to_remove = _find_arc_to_remove(continue_walk_response.get_cycle(), arcs)
        arcs.remove(arc_to_remove)
        remaining_unfinished_walks = _unfinished_walks_not_containing_arc(continue_walk_response.get_unfinished_walks(), arc_to_remove)
        _remove_remaining_forward_vertices_that_will_make_the_removed_arc(remaining_unfinished_walks, arc_to_remove)
        removed_arcs.add(arc_to_remove)
        for remaining_unfinished_walk in remaining_unfinished_walks:
            _eliminate_cycles_starting_from_walk(remaining_unfinished_walk, pattern_vertices, arcs)
    return removed_arcs

def _remove_remaining_forward_vertices_that_will_make_the_removed_arc(remaining_unfinished_walks: list[Walk], arc):
    for walk in remaining_unfinished_walks:
        last_vertex_of_walk = walk.walk[-1]
        remaining_forward_vertices = walk.get_remaining_forward_vertices()
        for forward_vertex in remaining_forward_vertices:
            if (last_vertex_of_walk, forward_vertex) == arc:
                new_remaining_forward_vertices = remaining_forward_vertices.copy()
                new_remaining_forward_vertices.remove(forward_vertex)
                walk.remaining_forward_vertices = new_remaining_forward_vertices
                return


def _unfinished_walks_not_containing_arc(unfinished_walks: list[Walk], arc):
    def unfinished_walk_does_not_contain_arc(unfinished_walk):
        return not _unfinished_walk_contains_arc(unfinished_walk, arc)
    return list(filter(unfinished_walk_does_not_contain_arc, unfinished_walks))

def _unfinished_walk_contains_arc(unfinished_walk, arc):
    unfinished_walk = unfinished_walk.walk
    last_index = len(unfinished_walk) - 1
    for index, vertex in enumerate(unfinished_walk):
        if index != last_index:
            next_vertex = unfinished_walk[index + 1]
            if (vertex, next_vertex) == arc:
                return True
    return False

def _continue_walk(walk: Walk, pattern_vertices, arcs) -> ContinueWalkResponse:
    forward_vertices: list[int] = walk.get_remaining_forward_vertices()
    if len(forward_vertices) == 0:
        return ContinueWalkResponse([], None)
    for index, forward_vertex in enumerate(forward_vertices):
        new_walk: Walk = Walk(walk.walk.copy(), None)
        add_vertex_result: AddVertexResult = new_walk.add_vertex(forward_vertex)
        if add_vertex_result.success:
            new_walk.remaining_forward_vertices = _forward_vertices(forward_vertex, pattern_vertices, arcs)
            continue_walk_response: ContinueWalkResponse = _continue_walk(new_walk, pattern_vertices, arcs)
            if continue_walk_response.cycle_encountered:
                unfinished_walks = continue_walk_response.get_unfinished_walks()
                last_index_forward_vertices = len(forward_vertices) - 1
                if index != last_index_forward_vertices:
                    unfinished_walks.append(Walk(walk.walk.copy(), forward_vertices[index + 1:]))
                return ContinueWalkResponse(unfinished_walks, continue_walk_response.get_cycle())
        else:
            unfinished_walks = []
            last_index_forward_vertices = len(forward_vertices) - 1
            if index != last_index_forward_vertices:
                unfinished_walks.append(Walk(walk.walk.copy(), forward_vertices[index + 1:]))
            return ContinueWalkResponse(unfinished_walks, add_vertex_result.get_cycle())
    return ContinueWalkResponse([], None)


def _find_arc_to_remove(cycle: tuple[int, ...], arcs: set[tuple[int, int]]):
    vertices_in_cycle: set[int] = set(cycle)
    for index, vertex in enumerate(cycle):
        if has_outgoing_arc_going_outside_cycle(vertex, vertices_in_cycle, arcs):
            next_vertex = cycle[(index + 1) % len(cycle)]
            return (vertex, next_vertex)
    raise ValueError('no arc found to remove')

def has_outgoing_arc_going_outside_cycle(vertex: int, vertices_in_cycle: set[int], arcs: set[tuple[int, int]]):
    filtered = filter(lambda arc: arc[0] == vertex and arc[1] not in vertices_in_cycle, arcs)
    return any(filtered)

def _forward_vertices(start_vertex: int, pattern_vertices: frozenset[int], arcs: set[tuple[int, int]]) -> list[int]:
    return list(map(lambda arc: arc[1], filter(lambda arc: arc[0] == start_vertex and arc[1] not in pattern_vertices, arcs)))

def _pick_one(vertices: Iterable[int]) -> int:
    return list(vertices)[0]
