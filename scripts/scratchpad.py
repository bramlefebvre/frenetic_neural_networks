
import numpy 



random_number_generator = numpy.random.default_rng()


vertices = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

a = random_number_generator.choice(vertices)

print(type(a))
