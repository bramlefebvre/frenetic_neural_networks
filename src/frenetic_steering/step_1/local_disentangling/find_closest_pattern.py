from frenetic_steering.application_on_images import load_images
from frenetic_steering.step_1.local_disentangling.util import number_of_spins_with_different_value


def find_closest_pattern():
    input = load_images.load_input()
    distances = []
    for i in range(load_images.get_number_of_patterns()):
        pattern = load_images.load_pattern(i)
        distances.append(number_of_spins_with_different_value(input, pattern))
    minimum_distance = min(distances)
    index_minimum = distances.index(minimum_distance)
    return (load_images.load_pattern(index_minimum), minimum_distance)
        
