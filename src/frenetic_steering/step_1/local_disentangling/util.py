



def number_of_spins_with_different_value(state_0, state_1):
    number_of_spins_with_different_value = 0
    for i, state_0_i in enumerate(state_0):
        if state_0_i != state_1[i]:
            number_of_spins_with_different_value += 1
    return number_of_spins_with_different_value