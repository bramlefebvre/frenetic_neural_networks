pattern_vertices = frozenset({0})

forward_vertices = [1, 2, 0]

forward_vertex_in_pattern_vertices = any(map(lambda forward_vertex: forward_vertex in pattern_vertices, forward_vertices))

print(forward_vertex_in_pattern_vertices)

a = 0
if a:
    print(3)