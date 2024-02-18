from frenetic_steering.application_on_images import load_images



def find_closest_pattern():
    input = load_images.load_input()
    distances = []
    for i in range(load_images.get_number_of_patterns()):
        pattern = load_images.load_pattern(i)
        distances.append(_number_of_spins_with_different_value(input, pattern))
    minimum_distance = min(distances)
    index_minimum = distances.index(minimum_distance)
    return (load_images.load_pattern(i), minimum_distance)
        
def _number_of_spins_with_different_value(state_1, state_2):
    number_of_spins_with_different_value = 0
    for i, state_1_i in enumerate(state_1):
        if state_1_i != state_2[i]:
            number_of_spins_with_different_value += 1
    return number_of_spins_with_different_value