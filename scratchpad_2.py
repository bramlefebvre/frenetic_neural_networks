from typing import NamedTuple

from step_2.data_structures import Action

class RateChangeInstruction(NamedTuple):
    transition: tuple[int, int]
    action: Action

a = RateChangeInstruction((1, 2), Action.INCREASE)

b = RateChangeInstruction((1, 2), Action.INCREASE)

c = {a}
c.add(b)
print(len(c))
print(a == b)
