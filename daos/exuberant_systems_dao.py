import daos.base_dao as base_dao
import numpy
from step_1.data_structures import CompletedBasin, ExuberantSystem

def get_single_exuberant_system(id, filename):
    serialized = base_dao.read_entry(id, filename)
    tournament_and_patterns_id = serialized['tournament_and_patterns_id']
    tournament = numpy.array(serialized['tournament'], dtype = int)
    basins = tuple(map(_deserialize_basin, serialized['basins']))
    return ExuberantSystem(tournament_and_patterns_id, tournament, basins, id)

def save_exuberant_system(exuberant_system, filename):
    serialized = _serialize_exuberant_system(exuberant_system)
    base_dao.add_single_entry_no_duplicates(serialized, filename)

def _serialize_exuberant_system(exuberant_system):
    serialized = {
        'tournament_and_patterns_id': exuberant_system.tournament_and_patterns_id,
        'tournament': exuberant_system.tournament.tolist(),
        'basins': list(map(_serialize_basin, exuberant_system.basins))
    }
    if exuberant_system.id is not None:
        serialized['id'] = exuberant_system.id
    return serialized 

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