
import numpy

from daos.graphs_and_patterns_dao import generate_single_graph_and_patterns
from step_1.find_disentangled_system import find_disentangled_system

random_number_generator = numpy.random.default_rng()

# graph_and_patterns = generate_single_graph_and_patterns(10, (frozenset({0}), frozenset({2})), 0.8)

# find_disentangled_system(graph_and_patterns)
graph = numpy.ones((5, 5), dtype=int)
# print(type(len(graph)))
a = 'ABCefg'
print(str.lower(a))