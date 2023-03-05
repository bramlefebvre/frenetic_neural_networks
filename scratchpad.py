
import numpy

from daos.graphs_and_patterns_dao import generate_single_graph_and_patterns
from step_1.find_disentangled_system import find_disentangled_system

random_number_generator = numpy.random.default_rng()

# graph_and_patterns = generate_single_graph_and_patterns(10, (frozenset({0}), frozenset({2})), 0.8)

# find_disentangled_system(graph_and_patterns)


a = [(1, 1), (1, 2), (1, 2, 3)]

def _pick_one_tuple(tuples: list[tuple[int, ...]]) -> tuple[int, ...]:
    index = random_number_generator.integers(len(tuples))
    return tuples[index]

print(type(_pick_one_tuple(a)))

