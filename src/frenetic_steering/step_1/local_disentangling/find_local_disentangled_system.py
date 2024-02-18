from frenetic_steering.application_on_images import load_images
from frenetic_steering.step_1.local_disentangling.find_closest_pattern import find_closest_pattern


def find_local_disentangled_system():
    pattern, distance = find_closest_pattern()
    cycle = _find_cycle(pattern)
    start_length_hair = _minimum_length_hair(input, cycle, distance)
    hair = _find_hair(cycle, input, start_length_hair)
    return _to_local_disentangled_system(cycle, hair)




