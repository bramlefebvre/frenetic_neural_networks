def flip_spin_value(spin_value):
    flipped_spin_value = 0
    if spin_value == 1:
        flipped_spin_value = 0
    else:
        flipped_spin_value = 1
    return flipped_spin_value


def number_of_neurons_with_different_value(state_0, state_1):
    number_of_spins_with_different_value = 0
    for i, state_0_i in enumerate(state_0):
        if state_0_i != state_1[i]:
            number_of_spins_with_different_value += 1
    return number_of_spins_with_different_value