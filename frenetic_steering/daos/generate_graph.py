'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2023 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''

import math
import numpy
from step_1.Moon_version.find_hamilton_cycle import hamilton_cycle_complete_tournament_exists
import numpy.typing as npt


random_number_generator = numpy.random.default_rng()


def generate_graph(number_of_states: int, fraction_of_arcs_present: float) -> npt.NDArray[numpy.int_]:
    graph: npt.NDArray[numpy.int_] = generate_tournament(number_of_states)
    edges_to_remove: set[tuple[int, int]] = _pick_edges_to_remove(number_of_states, fraction_of_arcs_present)
    for edge_to_remove in edges_to_remove:
        graph[edge_to_remove[0], edge_to_remove[1]] = -1
        graph[edge_to_remove[1], edge_to_remove[0]] = -1
    return graph


def generate_tournament(number_of_states: int) -> npt.NDArray[numpy.int_]:
    tournament: npt.NDArray[numpy.int_] = _generate_upper_half_random_tournament(number_of_states)
    _complete_tournament(tournament)
    return tournament

def generate_strong_tournament(number_of_states)-> npt.NDArray[numpy.int_]:
    found: bool = False
    tournament: npt.NDArray[numpy.int_] | None = None
    while not found:
        tournament = generate_tournament(number_of_states)
        found = hamilton_cycle_complete_tournament_exists(tournament)
    assert tournament is not None
    return tournament

def _pick_edges_to_remove(number_of_states: int, fraction_of_arcs_present: float) -> set[tuple[int, int]]:
    number_of_edges: int = number_of_states * (number_of_states - 1)/2 # type: ignore
    number_of_edges_to_remove: int = math.floor((1 - fraction_of_arcs_present) * number_of_edges)
    edges: set[tuple[int, int]] = _all_edges(number_of_states)
    edges_to_remove: set[tuple[int, int]] = set()
    while len(edges_to_remove) < number_of_edges_to_remove:
        edge: tuple[int, int] = _pick_one_edge(list(edges))
        edges.remove(edge)
        edges_to_remove.add(edge)
    return edges_to_remove


def _all_edges(number_of_states: int) -> set[tuple[int, int]]:
    all_edges: set[tuple[int, int]] = set([(i,j) for i in range(number_of_states) for j in range(number_of_states) if j>i])
    return all_edges

def _pick_one_edge(arcs: list[tuple[int, int]]) -> tuple[int, int]:
    return tuple(random_number_generator.choice(arcs))

def _generate_upper_half_random_tournament(number_of_states: int) -> npt.NDArray[numpy.int_]:
    tournament: npt.NDArray[numpy.int_] = -numpy.ones((number_of_states, number_of_states), dtype = int)
    for row in range(number_of_states):
        for column in range(number_of_states):
            if column > row:
                tournament[row, column] = random_number_generator.integers(2)
    return tournament

def _complete_tournament(tournament: npt.NDArray[numpy.int_]) -> None:
    number_of_states: int = len(tournament)
    for row in range(number_of_states):
        for column in range(number_of_states):
            if row > column:
                tournament[row, column] = _reverse(tournament[column, row])

def _reverse(value) -> int:
    if value == 0:
        return 1
    else:
        assert value == 1
        return 0