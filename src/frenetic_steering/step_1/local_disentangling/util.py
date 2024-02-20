



def number_of_spins_with_different_value(state_1, state_2):
    number_of_spins_with_different_value = 0
    for i, state_1_i in enumerate(state_1):
        if state_1_i != state_2[i]:
            number_of_spins_with_different_value += 1
    return number_of_spins_with_different_value