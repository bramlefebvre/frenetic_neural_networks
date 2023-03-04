


from daos.graphs_and_patterns_dao import generate_single_graph_and_patterns
from step_1.find_disentangled_system import find_disentangled_system



graph_and_patterns = generate_single_graph_and_patterns(10, (frozenset({0}), frozenset({2})), 0.8)

find_disentangled_system(graph_and_patterns)