

from step_2.data_structures import Action, RateChangeInstruction


print(RateChangeInstruction((1, 2), Action.INCREASE) == RateChangeInstruction((1, 2), Action.INCREASE))
