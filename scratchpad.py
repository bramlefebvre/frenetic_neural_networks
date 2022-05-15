import numpy

a = frozenset({1, 2, 3})

b = set(a)
b.remove(1)
print(b)
print(a)