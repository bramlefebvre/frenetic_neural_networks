from dataclasses import dataclass, field
from typing import Iterable

from step_1.data_structures import BasinUnderConstruction


def eliminate_cycles(basins: tuple[BasinUnderConstruction, ...], arcs: set[tuple[int, int]]):
    for basin in basins:
        _eliminate_cycles_for_basin(basin, arcs)


def _eliminate_cycles_for_basin(basin: BasinUnderConstruction, arcs: set[tuple[int, int]]):
    vertices_to_check: set[int] = basin.vertices_included_in_a_cycle - basin.pattern_vertices
    while len(vertices_to_check) > 0:
        start_vertex: int = _pick_one(vertices_to_check)
        forward_vertices = _forward_vertices_excluding_pattern_vertices(start_vertex, basin.pattern_vertices, arcs)
        path = Path([start_vertex], forward_vertices)
        number_of_vertices_in_basin = len(basin.pattern_vertices | basin.vertices_included_in_a_cycle)
        _eliminate_cycles_starting_from_path(path, basin.pattern_vertices, arcs, number_of_vertices_in_basin)
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


class Path:
    def __init__(self, path: list[int], remaining_forward_vertices: list[int] | None) -> None:
        self.path: list[int] = path
        self.vertices: set[int] = set(path)
        self.remaining_forward_vertices: list[int] | None = remaining_forward_vertices

    def add_vertex(self, vertex: int) -> AddVertexResult:
        if vertex in self.vertices:
            start_index_cycle: int = self.path.index(vertex)
            return AddVertexResult(tuple(self.path[start_index_cycle:]))
        else: 
            self.path.append(vertex)
            self.vertices.add(vertex)
            return AddVertexResult(None)

    def get_remaining_forward_vertices(self):
        if self.remaining_forward_vertices is None:
            raise ValueError('remaining_forward_vertices is None')
        return self.remaining_forward_vertices

@dataclass
class ContinuePathResponse:
    cycle_encountered: bool = field(init = False)
    unfinished_paths: list[Path]
    cycle: tuple[int, ...] | None

    def get_unfinished_paths(self) -> list[Path]:
        return self.unfinished_paths
    
    def get_cycle(self) -> tuple[int, ...]:
        if self.cycle is None:
            raise ValueError('cycle is None')
        return self.cycle

    def __post_init__(self):
        self.cycle_encountered = self.cycle is not None


def _eliminate_cycles_starting_from_path(path: Path, pattern_vertices: frozenset[int], arcs: set[tuple[int, int]], number_of_vertices_in_basin: int):
    continue_path_response = _continue_path(path, pattern_vertices, arcs)
    removed_arcs: set[tuple[int, int]] = set()
    if continue_path_response.cycle_encountered:
        arc_to_remove = _find_arc_to_remove(continue_path_response.get_cycle(), arcs, pattern_vertices, number_of_vertices_in_basin)
        arcs.remove(arc_to_remove)
        removed_arcs.add(arc_to_remove)
        unfinished_paths = _unfinished_paths_not_containing_arc(continue_path_response.get_unfinished_paths(), arc_to_remove)
        for unfinished_path in unfinished_paths:
            if not _unfinished_path_contains_arc_in_set(unfinished_path, removed_arcs):
                _remove_remaining_forward_vertices_that_will_make_a_removed_arc(unfinished_path, removed_arcs)
                new_removed_arcs = _eliminate_cycles_starting_from_path(unfinished_path, pattern_vertices, arcs, number_of_vertices_in_basin)
                removed_arcs.update(new_removed_arcs)
    return removed_arcs

def _remove_remaining_forward_vertices_that_will_make_a_removed_arc(unfinished_path: Path, removed_arcs):
    last_vertex_of_path = unfinished_path.path[-1]
    remaining_forward_vertices = unfinished_path.get_remaining_forward_vertices()
    forward_vertices_to_remove = set()
    for forward_vertex in remaining_forward_vertices:
        if (last_vertex_of_path, forward_vertex) in removed_arcs:
            forward_vertices_to_remove.add(forward_vertex)
    new_remaining_forward_vertices = list(set(remaining_forward_vertices) - forward_vertices_to_remove)
    unfinished_path.remaining_forward_vertices = new_remaining_forward_vertices

def _unfinished_paths_not_containing_arc(unfinished_paths: list[Path], arc: tuple[int, int]):
    def unfinished_path_does_not_contain_arc(unfinished_path):
        return not _unfinished_path_contains_arc_in_set(unfinished_path, {arc})
    return list(filter(unfinished_path_does_not_contain_arc, unfinished_paths))

def _unfinished_path_contains_arc_in_set(unfinished_path: Path, arcs):
    unfinished_path_path = unfinished_path.path
    last_index = len(unfinished_path_path) - 1
    for index, vertex in enumerate(unfinished_path_path):
        if index != last_index:
            next_vertex = unfinished_path_path[index + 1]
            if (vertex, next_vertex) in arcs:
                return True
    return False

def _continue_path(path: Path, pattern_vertices, arcs) -> ContinuePathResponse:
    forward_vertices: list[int] = path.get_remaining_forward_vertices()
    if len(forward_vertices) == 0:
        return ContinuePathResponse([], None)
    for index, forward_vertex in enumerate(forward_vertices):
        new_path: Path = Path(path.path.copy(), None)
        add_vertex_result: AddVertexResult = new_path.add_vertex(forward_vertex)
        if add_vertex_result.success:
            new_path.remaining_forward_vertices = _forward_vertices_excluding_pattern_vertices(forward_vertex, pattern_vertices, arcs)
            continue_path_response: ContinuePathResponse = _continue_path(new_path, pattern_vertices, arcs)
            if continue_path_response.cycle_encountered:
                unfinished_paths = continue_path_response.get_unfinished_paths()
                last_index_forward_vertices = len(forward_vertices) - 1
                if index != last_index_forward_vertices:
                    unfinished_paths.append(Path(path.path.copy(), forward_vertices[index + 1:]))
                return ContinuePathResponse(unfinished_paths, continue_path_response.get_cycle())
        else:
            unfinished_paths: list[Path] = []
            last_index_forward_vertices = len(forward_vertices) - 1
            if index != last_index_forward_vertices:
                unfinished_paths.append(Path(path.path.copy(), forward_vertices[index + 1:]))
            return ContinuePathResponse(unfinished_paths, add_vertex_result.get_cycle())
    return ContinuePathResponse([], None)


def _find_arc_to_remove(cycle: tuple[int, ...], arcs: set[tuple[int, int]], pattern_vertices: frozenset[int], number_of_vertices_in_basin: int):
    vertices_in_cycle: frozenset[int] = frozenset(cycle)
    length_of_path_to_pattern = 2
    while length_of_path_to_pattern <= number_of_vertices_in_basin:
        for index, vertex in enumerate(cycle):
            if _has_outgoing_path_outside_cycle_and_leading_to_pattern(vertex, vertices_in_cycle, arcs, pattern_vertices, length_of_path_to_pattern):
                next_vertex = cycle[(index + 1) % len(cycle)]
                return (vertex, next_vertex)
        length_of_path_to_pattern += 1
    raise ValueError('no arc found to remove')

def _has_outgoing_path_outside_cycle_and_leading_to_pattern(vertex: int, vertices_in_cycle: frozenset[int], arcs: set[tuple[int, int]], pattern_vertices: frozenset[int], length_of_path_to_pattern: int):
    path = Path([vertex], None)
    forward_vertices = _forward_vertices_excluding_vertices_in_cycle_and_vertices_in_path(vertex, vertices_in_cycle, path.vertices, arcs)
    path.remaining_forward_vertices = forward_vertices
    return _continue_path_to_pattern(path, vertices_in_cycle, arcs, pattern_vertices, length_of_path_to_pattern - 1)


def _continue_path_to_pattern(path: Path, vertices_in_cycle: frozenset[int], arcs: set[tuple[int, int]], pattern_vertices: frozenset[int], number_of_vertices_left: int):
    forward_vertices = path.get_remaining_forward_vertices()
    if len(forward_vertices) == 0:
        return False
    forward_vertices_contains_pattern_vertex = any(map(lambda forward_vertex: forward_vertex in pattern_vertices, forward_vertices))
    if forward_vertices_contains_pattern_vertex:
        return True
    if number_of_vertices_left == 1:
        return False
    for forward_vertex in forward_vertices:
        new_path_path = path.path.copy()
        new_path_path.append(forward_vertex)
        new_path: Path = Path(new_path_path, None)
        forward_vertices = _forward_vertices_excluding_vertices_in_cycle_and_vertices_in_path(forward_vertex, vertices_in_cycle, new_path.vertices, arcs)
        new_path.remaining_forward_vertices = forward_vertices
        pattern_encountered = _continue_path_to_pattern(new_path, vertices_in_cycle, arcs, pattern_vertices, number_of_vertices_left - 1)
        if pattern_encountered:
            return True
    return False


def _forward_vertices_excluding_vertices_in_cycle_and_vertices_in_path(start_vertex: int, vertices_in_cycle: frozenset[int], vertices_in_path: set[int], arcs: set[tuple[int, int]]):
    return list(map(lambda arc: arc[1], filter(lambda arc: arc[0] == start_vertex and arc[1] not in vertices_in_cycle and arc[1] not in vertices_in_path, arcs)))

def _forward_vertices_excluding_pattern_vertices(start_vertex: int, pattern_vertices: frozenset[int], arcs: set[tuple[int, int]]) -> list[int]:
    return list(map(lambda arc: arc[1], filter(lambda arc: arc[0] == start_vertex and arc[1] not in pattern_vertices, arcs)))

def _pick_one(vertices: Iterable[int]) -> int:
    return list(vertices)[0]
