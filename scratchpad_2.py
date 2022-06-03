a = set()
b = frozenset({3, 4})
c = frozenset({5, 6})

def do_something(set_1, set_2):
    set_1 |= set_2
    print(set_1)

d = (b, c)
a.update(*d)
print(a)
print(type(a))