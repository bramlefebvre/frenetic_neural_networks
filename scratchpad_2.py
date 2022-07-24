from typing import Any, Iterable


new = {1, 2, 3, 4}

def print_all(iterable: Iterable[Any]):
    for value in iterable:
        print(value)

print_all(new)

