import numpy

random_number_generator = numpy.random.default_rng()

a = random_number_generator.choice([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, replace=False)

print(a)