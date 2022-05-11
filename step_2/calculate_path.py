import numpy
import math

random_number_generator = numpy.random.default_rng()
# numpy.seterr(divide='ignore')

def calculate_path(rate_matrix, initial_state, total_travel_time):
    path = [(0, initial_state)]
    travel_time = 0
    state = initial_state
    while travel_time < total_travel_time:
        rates_for_state = rate_matrix[state, :]
        escape_rate = rates_for_state.sum()
        jump_time = random_number_generator.exponential(1/escape_rate)
        travel_time += jump_time
        if travel_time < total_travel_time:
            state = _decide_where_to_jump_to(rates_for_state, escape_rate)
            path.append((travel_time, state))
    datatype = numpy.dtype([('jump_time', float), ('state', int)])
    return numpy.array(path, datatype)


def _decide_where_to_jump_to(rates_for_state, escape_rate):
    number_of_states = len(rates_for_state)
    random_number = random_number_generator.random() * escape_rate
    summed_rates = numpy.cumsum(rates_for_state)
    left_search_boundary = 0
    right_search_boundary = number_of_states - 1
    index_to_check = math.floor(number_of_states / 2)
    while True:
        summed_rate = summed_rates[index_to_check]
        if random_number < summed_rate:
            if index_to_check == 0:
                # success index = 0
                return 0
            previous_summed_rate = summed_rates[index_to_check - 1]
            if random_number >= previous_summed_rate:
                # success index > 0
                return index_to_check
            else:
                # search more to the left
                right_search_boundary = index_to_check - 1
                index_to_check = math.floor((right_search_boundary - left_search_boundary) / 2) + left_search_boundary
        else:
            # assert index_to_check != number_of_states - 1
            if index_to_check == number_of_states - 1:
                assert escape_rate == numpy.Inf
                # should not be possible
                print('random number: ' + str(random_number))
                print('summed rates:')
                print(summed_rates)
                return summed_rates.tolist().index(numpy.Inf)
                

            # search more to the right
            left_search_boundary = index_to_check + 1
            index_to_check = math.floor((right_search_boundary - left_search_boundary) / 2) + left_search_boundary
