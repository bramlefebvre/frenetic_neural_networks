import daos.base_dao as base_dao
import numpy
from step_1.data_structures import CompletedBasin, ExuberantSystem

def get_single_exuberant_system(id, filename):
    serialized = base_dao.read_entry(id, filename)
    return _deserialize_exuberant_system(serialized)

def get_exuberant_systems(filename):
    serialized_exuberant_systems = base_dao.read_data(filename)
    return list(map(_deserialize_exuberant_system, serialized_exuberant_systems))

def save_exuberant_system(exuberant_system, filename):
    serialized = _serialize_exuberant_system(exuberant_system)
    base_dao.add_single_entry(serialized, filename)

def generate_cycle(number_of_states):
    graph = -numpy.ones((number_of_states, number_of_states), dtype = int)
    basins = (CompletedBasin(0, frozenset({0}), frozenset(range(number_of_states))),)
    for vertex in range(number_of_states):
        if vertex == number_of_states - 1:
            graph[vertex, 0] = 1
            graph[0, vertex] = 0
        else:
            graph[vertex, vertex + 1] = 1
            graph[vertex + 1, vertex] = 0
    return ExuberantSystem(None, graph, basins)

def _serialize_exuberant_system(exuberant_system):
    serialized = {
        'tournament_and_patterns_id': exuberant_system.tournament_and_patterns_id,
        'graph': exuberant_system.graph.tolist(),
        'basins': list(map(_serialize_basin, exuberant_system.basins))
    }
    if exuberant_system.id is not None:
        serialized['id'] = exuberant_system.id
    return serialized 

def _deserialize_exuberant_system(serialized):
    tournament_and_patterns_id = serialized['tournament_and_patterns_id']
    graph = numpy.array(serialized['graph'], dtype = int)
    basins = tuple(map(_deserialize_basin, serialized['basins']))
    id = serialized['id']
    return ExuberantSystem(tournament_and_patterns_id, graph, basins, id)

def _deserialize_basin(serialized):
    pattern_vertices = frozenset(serialized['pattern_vertices'])
    vertices = frozenset(serialized['vertices'])
    return CompletedBasin(serialized['index'], pattern_vertices, vertices)

def _serialize_basin(basin):
    pattern_vertices = list(basin.pattern_vertices)
    pattern_vertices.sort()
    vertices = list(basin.vertices)
    vertices.sort()
    serialized = {
        'index': basin.index,
        'pattern_vertices': pattern_vertices,
        'vertices': vertices
    }
    return serialized