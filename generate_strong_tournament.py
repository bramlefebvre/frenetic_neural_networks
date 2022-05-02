import numpy
from find_hamilton_cycle import hamilton_cycle_complete_tournament_exists

random_number_generator = numpy.random.default_rng()

def generate_random_strong_tournament(number_of_states):
    found = False
    while not found:
        tournament = _generate_random_tournament(number_of_states)
        found = hamilton_cycle_complete_tournament_exists(tournament)
    return tournament

def _generate_random_tournament(number_of_states):
    tournament = _generate_upper_half_random_tournament(number_of_states)
    _complete_tournament(tournament)
    return tournament

def _generate_upper_half_random_tournament(number_of_states):
    tournament = -numpy.ones((number_of_states, number_of_states))
    for row in range(number_of_states):
        for column in range(number_of_states):
            if column > row:
                tournament[row, column] = random_number_generator.integers(2)

def _complete_tournament(tournament):
    number_of_states = len(tournament)
    for row in range(number_of_states):
        for column in range(number_of_states):
            if row > column:
                tournament[row, column] = tournament[column, row]