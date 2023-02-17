import numpy
import numpy.typing as npt

from step_1.data_structures import BasinUnderConstruction
from step_1.find_disentangled_system import HairFindingProgressForBasin

random_number_generator = numpy.random.default_rng()

def find_hair(graph, hair_finding_progress_for_basin, basins: tuple[BasinUnderConstruction, ...]):
    free_vertices = _get_free_vertices(len(graph), basins)
    if len(free_vertices) == 0:
        pass
    path: tuple[int, ...] = ()
    _continue_path(path, graph, hair_finding_progress_for_basin, free_vertices)


def _continue_path(path, graph, hair_finding_progress_for_basin: HairFindingProgressForBasin, free_vertices):
    available_vertices = _get_forward_available_vertices(path, graph, free_vertices)
    
    if len(path) == 0:
        pass
    else:
        already_present_hair_vertices = _get_forward_already_present_hair_vertices(path, graph, hair_finding_progress_for_basin)


def _try_already_present_hair_vertex(path, hair_finding_progress_for_basin: HairFindingProgressForBasin, already_present_hair_vertex):
    number_of_vertices_left_to_add = hair_finding_progress_for_basin.length_of_hair_to_find - len(path)
    hair_finding_progress_for_basin.basin.arcs
    pass
    
def _number_of_vertices_on_hair_starting_from_already_present_hair_vertex(hair_finding_progress_for_basin: HairFindingProgressForBasin, already_present_hair_vertex):
    number = 1
    arcs = hair_finding_progress_for_basin.basin.arcs
    destination = _destination_arc_starting_from_vertex(arcs, already_present_hair_vertex)
    while destination in hair_finding_progress_for_basin.hair_vertices:
        number += 1
        destination = _destination_arc_starting_from_vertex(arcs, destination)
        

def _destination_arc_starting_from_vertex(arcs, vertex):
    destinations_of_arcs_starting_from_vertex = [arc[1] for arc in arcs if arc[0] == vertex]
    assert len(destinations_of_arcs_starting_from_vertex) == 1
    return destinations_of_arcs_starting_from_vertex[0]

def _get_forward_already_present_hair_vertices(path, graph, hair_finding_progress_for_basin: HairFindingProgressForBasin):
    last_vertex_of_path = path[-1]
    hair_vertices = [vertex for vertex in hair_finding_progress_for_basin.hair_vertices if graph[last_vertex_of_path, vertex] == 1]
    random_number_generator.shuffle(hair_vertices)
    return hair_vertices


def _get_free_vertices(number_of_vertices: int, basins: tuple[BasinUnderConstruction, ...]):
    vertices_in_a_basin = set()
    vertices_in_a_basin.update(*map(lambda x: x.vertices, basins))
    return frozenset(range(number_of_vertices)) - vertices_in_a_basin

def _get_forward_available_vertices(path, graph, free_vertices):
    last_vertex_of_path = path[-1]
    available_vertices = [vertex for vertex in set(free_vertices) - set(path) if graph[last_vertex_of_path, vertex] == 1]
    random_number_generator.shuffle(available_vertices)
    return available_vertices
