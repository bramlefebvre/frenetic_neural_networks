a = [1, 2, 3, 4, 5, 6, 7, 8]

index = 0
while len(a) > 0:
    print('inside while')
    print(a)
    a.remove(a[len(a) - 1])