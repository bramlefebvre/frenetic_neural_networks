import numpy

random_number_generator = numpy.random.default_rng()

a = {1, 2, 3}

def _pick_one(vertices):
    b = random_number_generator.choice(list(vertices))
    proposition = b == 1 | b == 2 | b == 3
    print(proposition)
    print(type(b), type(1))

c = random_number_generator.choice(5)
print('type c:')
print(type(c))
_pick_one(a)