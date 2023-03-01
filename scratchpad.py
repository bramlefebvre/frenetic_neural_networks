
from dataclasses import dataclass, field


a = {}

@dataclass
class DictTestClass:
    dict_field: dict[int, set[int]] = field(default_factory=dict)

test = DictTestClass()

test.dict_field[1] = {2, 3}
print(2 not in test.dict_field)