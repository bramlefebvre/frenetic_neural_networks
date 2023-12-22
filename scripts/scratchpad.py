import sys
import numpy

a = [1, 1, 1, 1, 1, 1, 1]

b = [True, True, False, False, True, True, False]

c = (8, 8)

test = numpy.zeros(10000, dtype=numpy.float32)

size = sys.getsizeof(test)

print(size)
