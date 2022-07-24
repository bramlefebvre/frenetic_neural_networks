from dataclasses import dataclass, field
from typing import Iterable

from step_1.data_structures import BasinUnderConstruction


def _cut_cycles(basins: tuple[BasinUnderConstruction, ...], arcs: set[tuple[int, int]]):
    
    pass

def _cut_cycles_for_basin(basin: BasinUnderConstruction, arcs: set[tuple[int, int]]):
    vertices_to_check: set[int] = set(basin.vertices_included_in_a_cycle - basin.pattern_vertices)
    while len(vertices_to_check) > 0:
        start_vertex: int = _pick_one(vertices_to_check)


def _find_all_walks_outside_pattern(basin: BasinUnderConstruction, start_vertex: int, vertices_to_check: set[int], arcs: set[tuple[int, int]]):
    walk = Walk()
    walk.add_vertex(start_vertex)


def _arcs_that_start_with_vertex():
    pass


def _pick_one(vertices: Iterable[int]):
    return list(vertices)[0]

class Walk:
    def __init__(self) -> None:
        self.walk: list[int] = []
        self.vertices: set[int] = set()

    def add_vertex(self, vertex: int):
        if vertex in self.vertices:
            start_index_cycle: int = self.walk.index(vertex)
            return AddVertexResult(tuple(self.walk[start_index_cycle:]))
        else: 
            self.walk.append(vertex)
            self.vertices.add(vertex)
            return AddVertexResult(None)

@dataclass
class AddVertexResult:
    success: bool = field(init = False)
    cycle: tuple[int, ...] | None

    def __post_init__(self):
        self.success = self.cycle is None