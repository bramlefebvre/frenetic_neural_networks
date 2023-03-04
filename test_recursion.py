

def recursive(a, sum):
    sum += a
    recursive(a-1, sum)


def iterative(a):
    sum = 0
    while a > 0:
        sum += a
