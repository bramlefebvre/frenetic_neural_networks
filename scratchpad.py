
import numpy

from daos.graphs_and_patterns_dao import generate_single_graph_and_patterns
from step_1.find_disentangled_system import find_disentangled_system

random_number_generator = numpy.random.default_rng()

# graph_and_patterns = generate_single_graph_and_patterns(10, (frozenset({0}), frozenset({2})), 0.8)

# find_disentangled_system(graph_and_patterns)

a = [1, 2, 3, 4, 5, 6, 7, 8]
random_number_generator.shuffle(a)
print(type(a))