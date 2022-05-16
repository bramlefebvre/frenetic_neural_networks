import numpy

random_number_generator = numpy.random.default_rng()

a = random_number_generator.choice([1, 2, 3])

print(type(a))