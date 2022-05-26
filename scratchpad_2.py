# def get_mean(getter, results):
#     data = list(map(getter, results))
#     return mean(data)

# def get_mean_duration(results):
#     get_mean(results, lambda x: x.calculation_duration)

def transform_data(getter, data):
    return list(map(getter, data))


class Container:
    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2


getter = lambda x: x.field_2
container = Container('value_1', 'value_2')

print(transform_data(getter, [container]))
